# app/utils/audio_utils.py
import wave
import contextlib
import re
import speech_recognition as sr

# ---------------- Audio Duration ----------------
def get_audio_duration(audio_path: str) -> float:
    """Return audio duration in seconds."""
    with contextlib.closing(wave.open(audio_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


# ---------------- Pauses & Filler Words ----------------
def count_pauses(audio_path: str, threshold: float = 1.0) -> int:
    """
    Count long pauses (> threshold seconds).
    Placeholder: Implement with real audio processing later.
    """
    # For MVP, return 0 as placeholder
    return 0


def count_filler_words(transcribed_text: str) -> int:
    """Count filler words like 'um', 'uh', 'like', 'you know'."""
    fillers = ['um', 'uh', 'like', 'you know', 'ah', 'er']
    words = transcribed_text.lower().split()
    count = sum(1 for w in words if w in fillers)
    return count


# ---------------- Pronunciation Score ----------------
def compute_pronunciation_score(transcribed_text: str, audio_path: str) -> float:
    """
    Simple heuristic:
    Compare number of words in audio vs transcribed text.
    For MVP, assume 0.8–1.0 if transcript exists, else lower.
    """
    if transcribed_text.strip():
        return 0.95  # placeholder, good enough for MVP
    return 0.5
