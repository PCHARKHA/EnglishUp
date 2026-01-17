from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.db.base import Base
from app.core.enums import AgeCategory, SkillType, DifficultyLevel
from sqlalchemy.orm import relationship

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)

    age_category = Column(Enum(AgeCategory, name="age_category_enum", native_enum=False), nullable=False)
    skill_type = Column(Enum(SkillType, name="skill_type_enum", native_enum=False), nullable=False)
    difficulty = Column(Enum(DifficultyLevel, name="difficulty_enum", native_enum=False), nullable=False)

    prompt_text = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    transcripts = relationship(
        "Transcript",
        back_populates="prompt",
        cascade="all, delete-orphan"
    )
