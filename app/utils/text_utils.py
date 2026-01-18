
import re
import language_tool_python
from textstat import flesch_kincaid_grade

# Initialize the grammar checker once
tool = language_tool_python.LanguageTool('en-US')


# ---------------- Text Tokenization ----------------
def tokenize_sentences(text: str):
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s for s in sentences if s]


def tokenize_words(text: str):
    """Split text into words (ignoring punctuation)."""
    words = re.findall(r'\b\w+\b', text.lower())
    return words


# ---------------- Grammar & Spelling ----------------
def count_grammar_errors(text: str) -> int:
    """Count grammar mistakes using LanguageTool."""
    matches = tool.check(text)
    # Filter only grammar mistakes (exclude style/writing suggestions if needed)
    grammar_errors = [m for m in matches if m.ruleIssueType == "grammar"]
    return len(grammar_errors)


def count_spelling_errors(text: str) -> int:
    """Count spelling mistakes using LanguageTool."""
    matches = tool.check(text)
    spelling_errors = [m for m in matches if m.ruleIssueType == "misspelling"]
    return len(spelling_errors)


# ---------------- Readability ----------------
def compute_readability(text: str) -> float:
    """Compute Flesch-Kincaid grade level."""
    try:
        score = flesch_kincaid_grade(text)
        return score
    except:
        return 0.0







