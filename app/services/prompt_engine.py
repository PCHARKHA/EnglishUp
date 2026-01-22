from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.prompt import Prompt
from app.core.enums import AgeCategory, SkillType, ProficiencyLevel,DifficultyLevel

def resolve_difficulty(proficiency: ProficiencyLevel) -> DifficultyLevel:
    if proficiency in (ProficiencyLevel.VERY_BASIC,
        ProficiencyLevel.BASIC,
    ):
        return DifficultyLevel.EASY

    if (proficiency == ProficiencyLevel.INTERMEDIATE):
        return DifficultyLevel.MEDIUM

    return DifficultyLevel.HARD

def get_prompt_for_user(        #the main logic
    db: Session,
    age_category: AgeCategory,
    proficiency: ProficiencyLevel,
    skill_type: SkillType,
):
    difficulty = resolve_difficulty(proficiency)

    prompt = (
        db.query(Prompt)
        .filter(
            Prompt.age_category == age_category,
            Prompt.skill_type == skill_type,
            Prompt.difficulty == difficulty,
            Prompt.is_active == True
        )
        .order_by(func.random())
        .first()
    )
    if not prompt:
        # Optional fallback if no prompt exists
        raise ValueError(f"No prompt found for {age_category}, {skill_type}, {difficulty}")

    return prompt
