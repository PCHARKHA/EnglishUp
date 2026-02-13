# app/api/v1/routers/progress.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.attempt import Attempt
from app.models.score import Score
from app.core.security import get_current_user
from app.schemas.score import ScoreResponse

router = APIRouter(
    prefix="/api/v1/progress",
    tags=["progress"],
)


# ------------------------------------------------
# Helper: level calculation
# ------------------------------------------------
def calculate_level(avg_score: float) -> str:
    if avg_score < 4:
        return "Beginner"
    if avg_score < 7:
        return "Improving"
    if avg_score < 9:
        return "Confident"
    return "Strong"


# ------------------------------------------------
# 1. Overall user progress
# ------------------------------------------------
@router.get("/me")
def get_user_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == current_user.id)
        .all()
    )

    if not attempts:
        return {
            "total_attempts": 0,
            "average_overall": 0,
            "level": "Beginner",
            "recent_scores": [],
        }

    attempt_ids = [a.id for a in attempts]

    scores = (
        db.query(Score)
        .filter(Score.attempt_id.in_(attempt_ids))
        .order_by(Score.created_at.desc())
        .all()
    )

    if not scores:
        return {
            "total_attempts": len(attempts),
            "average_overall": 0,
            "level": "Beginner",
            "recent_scores": [],
        }

    avg_overall = sum(s.overall for s in scores) / len(scores)

    return {
        "total_attempts": len(attempts),
        "average_overall": round(avg_overall, 2),
        "level": calculate_level(avg_overall),
        "recent_scores": [
            ScoreResponse.from_orm(s)
            for s in scores[:5]
        ],
    }


# ------------------------------------------------
# 2. Attempts history
# ------------------------------------------------
@router.get("/attempts")
def get_user_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == current_user.id)
        .order_by(Attempt.created_at.desc())
        .all()
    )

    attempt_ids = [a.id for a in attempts]

    scores = (
        db.query(Score)
        .filter(Score.attempt_id.in_(attempt_ids))
        .all()
    )

    score_map = {s.attempt_id: s for s in scores}

    return [
        {
            "attempt_id": a.id,
            "created_at": a.created_at,
            "score": (
                ScoreResponse.from_orm(score_map[a.id])
                if a.id in score_map
                else None
            ),
        }
        for a in attempts
    ]
