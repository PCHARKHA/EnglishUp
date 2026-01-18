# app/api/v1/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transcripts import Transcript
from app.services.language_analysis import LanguageAnalysisService
from app.services.speaking_analysis import SpeakingAnalysisService

router = APIRouter()

@router.get("/language/{transcript_id}")
def language_analysis(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    service = LanguageAnalysisService(transcript.response_text)
    return service.analyze()


@router.get("/speaking/{transcript_id}")
def speaking_analysis(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    if not transcript.audio_path:
        raise HTTPException(status_code=400, detail="No audio available for this transcript")

    service = SpeakingAnalysisService(transcript.response_text, transcript.audio_path)
    return service.analyze()


@router.get("/full/{transcript_id}")
def full_analysis(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    lang_service = LanguageAnalysisService(transcript.response_text)
    results = {"language": lang_service.analyze()}

    if transcript.audio_path:
        speak_service = SpeakingAnalysisService(transcript.response_text, transcript.audio_path)
        results["speaking"] = speak_service.analyze()
    
    return results
