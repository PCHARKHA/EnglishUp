# app/api/v1/routers/analysis.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.transcripts import Transcript
from app.services.language_analysis import LanguageAnalysisService
from app.services.speaking_analysis import SpeakingAnalysisService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/analysis",
    tags=["analysis"],
)


# ------------------------------------------------
# Helper: fetch transcript + ownership check
# ------------------------------------------------
def get_user_transcript(
    transcript_id: int,
    db: Session,
    current_user: User,
) -> Transcript:
    transcript = (
        db.query(Transcript)
        .filter(Transcript.id == transcript_id)
        .first()
    )

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    if transcript.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return transcript


# ------------------------------------------------
# Language analysis (text only)
# ------------------------------------------------
@router.get("/language/{transcript_id}")
def language_analysis(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transcript = get_user_transcript(transcript_id, db, current_user)

    service = LanguageAnalysisService(transcript.text)
    return {
        "transcript_id": transcript.id,
        "language_analysis": service.analyze(),
    }


# ------------------------------------------------
# Speaking analysis (audio required)
# ------------------------------------------------
@router.get("/speaking/{transcript_id}")
def speaking_analysis(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transcript = get_user_transcript(transcript_id, db, current_user)

    if not transcript.audio_path:
        raise HTTPException(
            status_code=400,
            detail="No audio available for this transcript",
        )

    service = SpeakingAnalysisService(
        transcript.text,
        transcript.audio_path,
    )

    return {
        "transcript_id": transcript.id,
        "speaking_analysis": service.analyze(),
    }


# ------------------------------------------------
# Full analysis (language + optional speaking)
# ------------------------------------------------
@router.get("/full/{transcript_id}")
def full_analysis(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transcript = get_user_transcript(transcript_id, db, current_user)

    results = {
        "transcript_id": transcript.id,
        "language": LanguageAnalysisService(
            transcript.text
        ).analyze(),
    }

    if transcript.audio_path:
        results["speaking"] = SpeakingAnalysisService(
            transcript.text,
            transcript.audio_path,
        ).analyze()

    return results
