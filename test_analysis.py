# test_analysis.py

from app.db.session import SessionLocal
from app.models.transcripts import Transcript
from app.services.language_analysis import LanguageAnalysisService
from app.services.speaking_analysis import SpeakingAnalysisService
import os

# ---------------- Setup DB ----------------
db = SessionLocal()

# ---------------- Create a Test Transcript ----------------
# Optional: Provide a sample audio file path for speaking test
audio_file = None  # e.g., "tests/sample_audio.wav" (ensure file exists)

test_text = (
    "This is a simple test sentence. "
    "We are checking if the language analysis works correctly. "
    "Hopefully, everything is fine!"
)

try:
    # Check if user_id=1 and prompt_id=1 exist (basic validation)
    from app.models.user import User
    from app.models.prompt import Prompt
    user = db.query(User).filter(User.id == 1).first()
    prompt = db.query(Prompt).filter(Prompt.id == 1).first()
    if not user or not prompt:
        raise ValueError("Test user or prompt not found. Seed DB first.")

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
    if audio_file and os.path.exists(audio_file):
        speak_service = SpeakingAnalysisService(transcript.text, transcript.audio_path)
        speak_metrics = speak_service.analyze()
        print("\n--- Speaking Analysis Metrics ---")
        for k, v in speak_metrics.items():
            print(f"{k}: {v}")
    else:
        print("\nNo valid audio provided; skipping speaking analysis.")

except Exception as e:
    print(f"Error during testing: {e}")
    db.rollback()

finally:
    # ---------------- Clean Up ----------------
    try:
        db.delete(transcript)
        db.commit()
    except:
        pass  # Ignore if already deleted or error
    db.close()

print("Test completed.")