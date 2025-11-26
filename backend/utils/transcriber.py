from transformers import pipeline
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/
WHISPER_DIR = os.path.join(BASE_DIR, "..", "models", "whisper_saved")

asr = pipeline(
    "automatic-speech-recognition",
    model=WHISPER_DIR,
    tokenizer=WHISPER_DIR,
    feature_extractor=WHISPER_DIR,
)

def transcribe_audio(audio_path):
    result = asr(audio_path)
    return result["text"]
