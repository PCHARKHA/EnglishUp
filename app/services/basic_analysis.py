import re

class BasicAnalysisService:
    @staticmethod
    def analyze(text: str) -> dict:
        sentences = re.split(r'[.!?]+', text.strip())
        sentences = [s for s in sentences if s.strip()]

        words = re.findall(r'\b\w+\b', text)

        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = (
            round(word_count / sentence_count, 2) if sentence_count > 0 else 0
        )

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
        }
