# app/schemas/evaluate.py
from pydantic import BaseModel, Field, root_validator
from typing import Optional
from app.core.enums import AgeCategory, ProficiencyLevel, SkillType


class EvaluateRequest(BaseModel):
    """
    Request sent when user asks for a prompt to solve.
    """
    age: int = Field(..., ge=5, le=100)
    proficiency: int = Field(..., ge=1, le=5)
    skill_type: SkillType


class SubmitResponseSchema(BaseModel):
    """
    Schema for submitting a user response (text or audio).
    """
    user_id: int
    prompt_id: int
    text_response: Optional[str] = None
    
    @root_validator
    def check_text(cls, values):
        text = values.get("text_response")
    
        if not text :
            raise ValueError("Either text_response or audio_file must be provided")

        if text:
            stripped_text = text.strip()
            if len(stripped_text) == 0:
                raise ValueError("Text response cannot be empty")
            if len(stripped_text) > 2000:
                raise ValueError("Text response too long (max 2000 chars)")

        return values
