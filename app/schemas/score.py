from pydantic import BaseModel
from typing import Optional
from enum import Enum


# ENGLISHUP-SPECIFIC: evaluation type
class EvaluationType(str, Enum):
    speaking = "speaking"
    writing = "writing"


# GENERIC STRUCTURE: base score fields
class BaseScore(BaseModel):
    grammar: float
    coherence: float
    overall: float


# ENGLISHUP-SPECIFIC: speaking metrics
class SpeakingScore(BaseScore):
    fluency: float
    pronunciation: float


# ENGLISHUP-SPECIFIC: writing metrics
class WritingScore(BaseScore):
    vocabulary: float
    task_relevance: float


# GENERIC API RESPONSE PATTERN
class ScoreResponse(BaseModel):
    attempt_id: int
    evaluation_type: EvaluationType
    score: dict
