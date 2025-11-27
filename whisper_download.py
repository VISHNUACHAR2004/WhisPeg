from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

# Model name
name = "openai/whisper-base"

# Download processor (tokenizer + feature extractor)
processor = AutoProcessor.from_pretrained(name)

# Download Whisper model
model = AutoModelForSpeechSeq2Seq.from_pretrained(name)

# Save both to your target folder
save_path = "V:/projects/WhisPeg/models/whisper_saved"

processor.save_pretrained(save_path)
model.save_pretrained(save_path)

print("Whisper model downloaded and saved correctly!")
