from transformers import pipeline

WHISPER_DIR = "V:/projects/WhisPeg/models/whisper_saved"

asr = pipeline(
    "automatic-speech-recognition",
    model=WHISPER_DIR,
    tokenizer=WHISPER_DIR,
    feature_extractor=WHISPER_DIR
)

def transcribe_audio(audio_path):
    output = asr(audio_path)
    return output["text"]
