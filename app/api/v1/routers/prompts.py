# app/api/v1/routers/prompts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.prompt import Prompt
from app.schemas.evaluate import EvaluateRequest
from app.services.prompt_engine import get_prompt_for_user
from app.utils.age import get_age_category
from app.utils.proficiency import get_proficiency_level

router = APIRouter(
    prefix="/api/v1/prompts",
    tags=["Prompts"]
)

# --------------------------------------------------
# CORE ENDPOINT — FETCH PROMPT FOR USER
# --------------------------------------------------
@router.post("/get")
def get_prompt(data: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Returns a single prompt based on:
    - age
    - proficiency
    - skill type
    """
    try:
        age_category = get_age_category(data.age)
        proficiency = get_proficiency_level(data.proficiency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        prompt = get_prompt_for_user(
            db=db,
            age_category=age_category,
            proficiency=proficiency,
            skill_type=data.skill_type,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "prompt_id": prompt.id,
        "prompt_text": prompt.prompt_text,
        "skill_type": prompt.skill_type,
        "difficulty": prompt.difficulty,
        "age_category": prompt.age_category,
    }


# --------------------------------------------------
# ADMIN / DEBUG — LIST ALL PROMPTS
# --------------------------------------------------
@router.get("/all")
def list_all_prompts(db: Session = Depends(get_db)):
    """
    Returns all prompts (admin/debug use).
    """
    prompts = db.query(Prompt).all()
    return [
        {
            "id": p.id,
            "age_category": p.age_category,
            "skill_type": p.skill_type,
            "difficulty": p.difficulty,
            "prompt_text": p.prompt_text,
            "is_active": p.is_active,
        }
        for p in prompts
    ]


# --------------------------------------------------
# ADMIN — ENABLE / DISABLE PROMPT
# --------------------------------------------------
@router.patch("/{prompt_id}/toggle")
def toggle_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """
    Soft enable/disable a prompt.
    """
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()

    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    prompt.is_active = not prompt.is_active
    db.commit()
    db.refresh(prompt)

    return {
        "prompt_id": prompt.id,
        "is_active": prompt.is_active
    }
