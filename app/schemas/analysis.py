# schemas/analysis.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.schemas.score import EvaluationType

class LanguageAnalysisResponse(BaseModel):
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    grammar_errors: int
    spelling_errors: int
    vocabulary_richness: float
    readability_score: float
    long_sentences: int

class SpeakingAnalysisResponse(BaseModel):
    total_duration: float
    words_per_minute: float
    filler_words_count: int
    pauses_count: int
    pronunciation_score: float
    fluency_score: float
    clarity_score: float

class FullAnalysisResponse(BaseModel):
    language: LanguageAnalysisResponse
    speaking: Optional[SpeakingAnalysisResponse] = None
    feedback: Dict[str, List[str]]  # e.g., {"speaking": ["Reduce fillers..."], "grammar": [...]}

class AnalysisRequest(BaseModel):
    transcript_id: int
    evaluation_type: EvaluationType  # speaking or writing