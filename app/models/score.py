from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)

    # Link score to an attempt
    attempt_id = Column(Integer, ForeignKey("attempts.id"), nullable=False)

    # ENGLISHUP-SPECIFIC: speaking / writing
    evaluation_type = Column(String, nullable=False)

    # Common metrics
    grammar = Column(Float, nullable=False)
    coherence = Column(Float, nullable=False)

    # Speaking-only metrics (nullable for writing)
    fluency = Column(Float, nullable=True)
    pronunciation = Column(Float, nullable=True)

    # Writing-only metrics (nullable for speaking)
    vocabulary = Column(Float, nullable=True)
    task_relevance = Column(Float, nullable=True)

    # Overall score
    overall = Column(Float, nullable=False)

    # Relationship back to attempt
    attempt = relationship("Attempt", back_populates="score")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
