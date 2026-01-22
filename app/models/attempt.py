# models/attempt.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transcript_id = Column(Integer, ForeignKey("transcripts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="attempts")  # Assumes User has attempts relationship
    transcript = relationship("Transcript", back_populates="attempts")  # Assumes Transcript has attempts relationship
    score = relationship("Score", back_populates="attempt", uselist=False)  # One score per attempt