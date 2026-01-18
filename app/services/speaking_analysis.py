# app/services/speaking_analysis.py
from app.utils.audio_utils import get_audio_duration, count_pauses, count_filler_words, compute_pronunciation_score

class SpeakingAnalysisService:
    def __init__(self, text: str, audio_path: str):
        self.text = text
        self.audio_path = audio_path

    def analyze(self):
        total_duration = get_audio_duration(self.audio_path)
        filler_words_count = count_filler_words(self.text)
        pauses_count = count_pauses(self.audio_path)
        pronunciation_score = compute_pronunciation_score(self.text, self.audio_path)

        words = self.text.split()
        words_per_minute = len(words) / (total_duration / 60) if total_duration > 0 else 0
        fluency_score = max(0, min(1, 1 - (pauses_count / max(len(words), 1))))  # simple heuristic
        clarity_score = pronunciation_score  # for now same as pronunciation

        return {
            "total_duration": round(total_duration, 2),
            "words_per_minute": round(words_per_minute, 2),
            "filler_words_count": filler_words_count,
            "pauses_count": pauses_count,
            "pronunciation_score": round(pronunciation_score, 2),
            "fluency_score": round(fluency_score, 2),
            "clarity_score": round(clarity_score, 2)
        }
