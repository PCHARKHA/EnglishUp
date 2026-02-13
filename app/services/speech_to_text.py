# app/services/speech_to_text.py
import whisper

class SpeechToTextService:
    """
    Service for converting audio to text using OpenAI Whisper.
    """
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper model.
        Args:
            model_name (str): Whisper model variant ('tiny', 'base', 'small', 'medium', 'large')
        """
        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model '{model_name}': {e}")

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text.
        Args:
            audio_path (str): Path to the audio file
        Returns:
            str: Transcribed text
        """
        try:
            result = self.model.transcribe(audio_path)
            text = result.get("text", "").strip()
            return text
        except Exception as e:
            # Return empty string on failure, caller can handle
            print(f"Error during transcription: {e}")
            return ""
