# test_analysis.py
from app.db.session import SessionLocal
from app.models.transcripts import Transcript
from app.services.language_analysis import LanguageAnalysisService
from app.services.speaking_analysis import SpeakingAnalysisService
import os

# ---------------- Setup DB ----------------
db = SessionLocal()

# ---------------- Create a Test Transcript ----------------
# Use a small audio file if you want speaking metrics, or leave None for text-only
audio_file = None  # Example: "tests/sample_audio.wav" if available

test_text = (
    "This is a simple test sentence. "
    "We are checking if the language analysis works correctly. "
    "Hopefully, everything is fine!"
)

transcript = Transcript(
    user_id=1,
    prompt_id=1,
    text=test_text,
    input_mode="text" if not audio_file else "speech",
    audio_path=audio_file
)

db.add(transcript)
db.commit()
db.refresh(transcript)

print(f"Created test transcript with ID: {transcript.id}")

# ---------------- Run Language Analysis ----------------
lang_service = LanguageAnalysisService(transcript.text)
lang_metrics = lang_service.analyze()
print("\n--- Language Analysis Metrics ---")
for k, v in lang_metrics.items():
    print(f"{k}: {v}")

# ---------------- Run Speaking Analysis ----------------
if audio_file:
    speak_service = SpeakingAnalysisService(transcript.text, transcript.audio_path)
    speak_metrics = speak_service.analyze()
    print("\n--- Speaking Analysis Metrics ---")
    for k, v in speak_metrics.items():
        print(f"{k}: {v}")
else:
    print("\nNo audio provided; skipping speaking analysis.")

# ---------------- Clean Up ----------------
db.delete(transcript)
db.commit()
db.close()
