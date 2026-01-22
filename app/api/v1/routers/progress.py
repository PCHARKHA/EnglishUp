# app/api/v1/routers/progress.py
# app/api/v1/routers/progress.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.attempt import Attempt
from app.models.score import Score
from app.core.security import get_current_user
from app.schemas.score import ScoreResponse

router = APIRouter()

@router.get("/my_progress", response_model=dict)
def get_user_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's overall progress: total attempts, average scores, current level.
    """
    attempts = db.query(Attempt).filter(Attempt.user_id == current_user.id).all()
    if not attempts:
        return {"message": "No attempts yet. Start practicing!"}
    
    scores = [db.query(Score).filter(Score.attempt_id == a.id).first() for a in attempts if a.score]
    scores = [s for s in scores if s]  # Filter None
    
    if not scores:
        return {"total_attempts": len(attempts), "average_overall": 0, "level": "Beginner"}
    
    avg_overall = sum(s.overall for s in scores) / len(scores)
    level = "Beginner" if avg_overall < 4 else "Improving" if avg_overall < 7 else "Confident" if avg_overall < 9 else "Strong"
    
    return {
        "total_attempts": len(attempts),
        "average_overall": round(avg_overall, 2),
        "level": level,
        "recent_scores": [ScoreResponse.from_orm(s) for s in scores[-5:]]  # Last 5
    }

@router.get("/attempts", response_model=List[dict])
def get_user_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of user's attempts with scores."""
    attempts = db.query(Attempt).filter(Attempt.user_id == current_user.id).all()
    result = []
    for a in attempts:
        score = db.query(Score).filter(Score.attempt_id == a.id).first()
        result.append({
            "attempt_id": a.id,
            "created_at": a.created_at,
            "score": ScoreResponse.from_orm(score) if score else None
        })
    return result