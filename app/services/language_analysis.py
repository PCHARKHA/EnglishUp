# app/services/language_analysis.py
from app.utils.text_utils import tokenize_sentences, tokenize_words, count_grammar_errors, count_spelling_errors, compute_readability

class LanguageAnalysisService:
    def __init__(self, text: str):
        self.text = text

    def analyze(self):
        sentences = tokenize_sentences(self.text)
        words = tokenize_words(self.text)
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        grammar_errors = count_grammar_errors(self.text)
        spelling_errors = count_spelling_errors(self.text)
        vocabulary_richness = len(set(words)) / word_count if word_count > 0 else 0
        readability_score = compute_readability(self.text)
        long_sentences = sum(1 for s in sentences if len(tokenize_words(s)) > 20)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "grammar_errors": grammar_errors,
            "spelling_errors": spelling_errors,
            "vocabulary_richness": round(vocabulary_richness, 2),
            "readability_score": round(readability_score, 2),
            "long_sentences": long_sentences
        }
