from typing import Dict
from app.schemas.score import EvaluationType


class ScoringService:
    """
    Responsible ONLY for calculating numeric scores.
    No DB logic.
    No feedback generation.
    """

    @staticmethod
    def calculate_speaking_score(analysis_data: Dict) -> Dict:
        """
        analysis_data is expected to contain pre-extracted signals
        like grammar_errors, pauses, pronunciation_score, coherence_score
        """

        grammar = max(0.0, 10.0 - analysis_data.get("grammar_errors", 0))
        fluency = analysis_data.get("fluency", 5.0)
        pronunciation = analysis_data.get("pronunciation", 5.0)
        coherence = analysis_data.get("coherence", 5.0)

        overall = round(
            (grammar + fluency + pronunciation + coherence) / 4, 2
        )

        return {
            "evaluation_type": EvaluationType.speaking,
            "grammar": grammar,
            "fluency": fluency,
            "pronunciation": pronunciation,
            "coherence": coherence,
            "overall": overall,
        }

    @staticmethod
    def calculate_writing_score(analysis_data: Dict) -> Dict:
        """
        analysis_data is expected to contain signals
        like grammar_errors, vocabulary_score, relevance_score, coherence_score
        """

        grammar = max(0.0, 10.0 - analysis_data.get("grammar_errors", 0))
        vocabulary = analysis_data.get("vocabulary", 5.0)
        coherence = analysis_data.get("coherence", 5.0)
        task_relevance = analysis_data.get("task_relevance", 5.0)

        overall = round(
            (grammar + vocabulary + coherence + task_relevance) / 4, 2
        )

        return {
            "evaluation_type": EvaluationType.writing,
            "grammar": grammar,
            "vocabulary": vocabulary,
            "coherence": coherence,
            "task_relevance": task_relevance,
            "overall": overall,
        }
