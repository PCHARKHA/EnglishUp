# app/routes/evaluate.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.db.session import get_db
from app.schemas.evaluate import EvaluateRequest, SubmitResponseSchema
from app.services.prompt_engine import get_prompt
from app.utils.age import get_age_category
from app.utils.proficiency import get_proficiency_level
from app.services.speech_to_text import SpeechToTextService
from app.models.transcripts import Transcript
from app.services.basic_analysis import BasicAnalysisService

router = APIRouter()

# --- /evaluate endpoint ---
@router.post("/evaluate")
def evaluate(data: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Returns a prompt based on user's age, proficiency, and skill type.
    """
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
        raise HTTPException(status_code=404, detail="No prompt found for the given criteria")

    return {
        "prompt_id": prompt.id,
        "prompt_text": prompt.prompt_text,
        "skill_type": data.skill_type,
    }


# --- Setup for /submit_response endpoint ---
speech_service = SpeechToTextService()
UPLOAD_DIR = "uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/submit_response")
async def submit_response(
    data: SubmitResponseSchema = Depends(),
    audio_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Accepts user response as text or audio, transcribes if needed, stores temporarily in DB.
    """
    # Validation rules
    if audio_file and data.text_response:
        raise HTTPException(status_code=400, detail="Provide either text or audio, not both")
    if not audio_file and not data.text_response:
        raise HTTPException(status_code=400, detail="Text or audio is required")

    response_text = ""
    response_type = "text"
    audio_path = None

    # --- Case 1: Text input ---
    if data.text_response:
        response_text = data.text_response.strip()

    # --- Case 2: Audio input ---
    if audio_file:
        response_type = "speech"
        filename = f"{uuid.uuid4()}_{audio_file.filename}"
        audio_path = os.path.join(UPLOAD_DIR, filename)

        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        response_text = speech_service.transcribe(audio_path)

        if not response_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

    # --- Temporary DB storage ---
    user_response = Transcript(
        user_id=data.user_id,
        prompt_id=data.prompt_id,
        text=response_text,
        input_mode=response_type,
        audio_path=audio_path
    )

    db.add(user_response)
    db.commit()
    db.refresh(user_response)

    # --- Return response info (ready for evaluation) ---
    return {
        "response_id": user_response.id,
        "text": response_text,
    
        }

@router.get("/analysis/{transcript_id}")
def analyze_transcript(transcript_id: int, db: Session = Depends(get_db)):
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
    
