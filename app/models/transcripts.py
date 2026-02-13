from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)

    # Ownership
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attempt_id = Column(Integer, ForeignKey("attempts.id"), nullable=False)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)

    # Content
    text = Column(Text, nullable=False)  # final text (typed or whisper output)
    input_mode = Column(String(10), nullable=False)  # "text" | "speech"
    audio_path = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="transcripts")
    attempt = relationship("Attempt", back_populates="transcripts", cascade="all, delete-orphan")
    prompt = relationship("Prompt", back_populates="transcripts")
