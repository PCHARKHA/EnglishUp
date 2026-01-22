# app/api/v1/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transcripts import Transcript
from app.services.language_analysis import LanguageAnalysisService
from app.services.speaking_analysis import SpeakingAnalysisService
from app.core.security import get_current_user  # Add this import
from app.models.user import User  # Add if needed for ownership checks

router = APIRouter()

@router.get("/language/{transcript_id}")
def language_analysis(
    transcript_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Add auth dependency
):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    # Optional: Check ownership (ensure transcript belongs to current user)
    if transcript.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    service = LanguageAnalysisService(transcript.text)
    return service.analyze()

@router.get("/speaking/{transcript_id}")
def speaking_analysis(
    transcript_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Add auth dependency
):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    # Optional: Check ownership
    if transcript.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not transcript.audio_path:
        raise HTTPException(status_code=400, detail="No audio available for this transcript")
    
    service = SpeakingAnalysisService(transcript.text, transcript.audio_path)
    return service.analyze()

@router.get("/full/{transcript_id}")
def full_analysis(
    transcript_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # Add auth dependency
):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    # Optional: Check ownership
    if transcript.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    lang_service = LanguageAnalysisService(transcript.text)
    results = {"language": lang_service.analyze()}
    
    if transcript.audio_path:
        speak_service = SpeakingAnalysisService(transcript.text, transcript.audio_path)
        results["speaking"] = speak_service.analyze()
    
    return results