# app/api/v1/routers/evaluate.py

from fastapi import (APIRouter,Depends,HTTPException,UploadFile,File,Form,)
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.db.session import get_db
from app.schemas.evaluate import EvaluateRequest
from app.schemas.score import ScoreResponse, EvaluationType
from app.services.prompt_engine import get_prompt
from app.utils.age import get_age_category
from app.utils.proficiency import get_proficiency_level
from app.services.speech_to_text import SpeechToTextService
from app.services.basic_analysis import BasicAnalysisService
from app.services.scoring import ScoringService

from app.models.transcripts import Transcript
from app.models.attempt import Attempt
from app.models.score import Score

router = APIRouter(
    prefix="/api/v1/evaluate",
    tags=["evaluation"],
)

speech_service = SpeechToTextService()

UPLOAD_DIR = "uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------------------------------
# 1. Get prompt
# ------------------------------------------------
@router.post("/prompt")
def get_evaluation_prompt(
    data: EvaluateRequest,
    db: Session = Depends(get_db),
):
    try:
        age_category = get_age_category(data.age)
        proficiency = get_proficiency_level(data.proficiency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    prompt = get_prompt(
        db=db,
        age_category=age_category,
        proficiency=proficiency,
        skill_type=data.skill_type,
    )

    if not prompt:
        raise HTTPException(status_code=404, detail="No prompt found")

    return {
        "prompt_id": prompt.id,
        "prompt_text": prompt.prompt_text,
        "skill_type": data.skill_type,
    }


# ------------------------------------------------
# 2. Submit response (text or speech)
# ------------------------------------------------
@router.post("/submit")
async def submit_response(
    user_id: int = Form(...),
    prompt_id: int = Form(...),
    text_response: str | None = Form(None),
    audio_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    if audio_file and text_response:
        raise HTTPException(
            status_code=400,
            detail="Provide either text or audio, not both",
        )

    if not audio_file and not text_response:
        raise HTTPException(
            status_code=400,
            detail="Text or audio is required",
        )

    response_text = ""
    input_mode = "text"
    audio_path = None

    if text_response:
        response_text = text_response.strip()

    if audio_file:
        input_mode = "speech"
        filename = f"{uuid.uuid4()}_{audio_file.filename}"
        audio_path = os.path.join(UPLOAD_DIR, filename)

        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        response_text = speech_service.transcribe(audio_path)

        if not response_text:
            raise HTTPException(
                status_code=400,
                detail="Could not transcribe audio",
            )

    transcript = Transcript(
        user_id=user_id,
        prompt_id=prompt_id,
        text=response_text,
        input_mode=input_mode,
        audio_path=audio_path,
    )

    try:
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
    except Exception:
        db.rollback()
        raise

    return {
        "transcript_id": transcript.id,
        "text": response_text,
    }


# ------------------------------------------------
# 3. Analyze transcript
# ------------------------------------------------
@router.get("/analysis/{transcript_id}")
def analyze_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
):
    transcript = (
        db.query(Transcript)
        .filter(Transcript.id == transcript_id)
        .first()
    )

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    analysis = BasicAnalysisService.analyze(transcript.text)

    return {
        "transcript_id": transcript.id,
        "analysis": analysis,
    }


# ------------------------------------------------
# 4. Final scoring
# ------------------------------------------------
@router.post("/score", response_model=ScoreResponse)
def evaluate_attempt(
    attempt_id: int,
    evaluation_type: EvaluationType,
    analysis_data: dict,
    db: Session = Depends(get_db),
):
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if evaluation_type == EvaluationType.speaking:
        score_data = ScoringService.calculate_speaking_score(analysis_data)
    else:
        score_data = ScoringService.calculate_writing_score(analysis_data)

    score = Score(
        attempt_id=attempt.id,
        evaluation_type=evaluation_type.value,
        grammar=score_data["grammar"],
        coherence=score_data["coherence"],
        fluency=score_data.get("fluency"),
        pronunciation=score_data.get("pronunciation"),
        vocabulary=score_data.get("vocabulary"),
        task_relevance=score_data.get("task_relevance"),
        overall=score_data["overall"],
    )

    try:
        db.add(score)
        db.commit()
        db.refresh(score)
    except Exception:
        db.rollback()
        raise

    return ScoreResponse(
        attempt_id=attempt.id,
        evaluation_type=evaluation_type,
        score=score_data,
    )
