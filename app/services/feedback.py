# services/feedback.py
from typing import Dict, List
from app.schemas.score import EvaluationType

class FeedbackService:
    @staticmethod
    def generate_feedback(analysis_data: Dict, score_data: Dict, evaluation_type: EvaluationType) -> Dict[str, List[str]]:
        """
        Generate 2-3 actionable suggestions with tags: speaking, grammar, vocabulary.
        Based on analysis data (from services) and score data (from ScoringService).
        """
        suggestions = {"speaking": [], "grammar": [], "vocabulary": []}
        
        # Speaking-specific feedback
        if evaluation_type == EvaluationType.speaking:
            if score_data.get("fluency", 5) < 5:
                suggestions["speaking"].append("Practice speaking slowly to reduce fillers like 'um' or 'uh'.")
            if score_data.get("pronunciation", 5) < 5:
                suggestions["speaking"].append("Focus on clear pronunciation—record and listen to yourself.")
            if analysis_data.get("words_per_minute", 150) > 200:
                suggestions["speaking"].append("Slow down your speech for better clarity.")
        
        # Grammar feedback (applies to both speaking/writing)
        if score_data.get("grammar", 5) < 5:
            grammar_errors = analysis_data.get("grammar_errors", 0)
            if grammar_errors > 2:
                suggestions["grammar"].append("Review common grammar rules, like tense agreement.")
            else:
                suggestions["grammar"].append("Check sentence structure in your responses.")
        
        # Vocabulary feedback (applies to both)
        if analysis_data.get("vocabulary_richness", 0.5) < 0.3 or score_data.get("vocabulary", 5) < 5:
            suggestions["vocabulary"].append("Expand your vocabulary by learning 5 new words daily.")
            if evaluation_type == EvaluationType.writing:
                suggestions["vocabulary"].append("Use more varied words in writing—try synonyms.")
        
        # Ensure at least 2-3 suggestions total
        all_suggestions = suggestions["speaking"] + suggestions["grammar"] + suggestions["vocabulary"]
        if len(all_suggestions) < 2:
            if evaluation_type == EvaluationType.speaking:
                suggestions["speaking"].append("Record yourself more often to build confidence.")
            else:
                suggestions["grammar"].append("Read English texts to improve grammar naturally.")
        
        # Limit to 3 per category for brevity
        for key in suggestions:
            suggestions[key] = suggestions[key][:3]
        
        return suggestions