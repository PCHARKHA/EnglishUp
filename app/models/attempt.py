from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="attempts")

    prompt = relationship("Prompt")

    transcripts = relationship(
        "Transcript",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )

    score = relationship(
        "Score",
        back_populates="attempt",
        uselist=False,
        cascade="all, delete-orphan"
    )
