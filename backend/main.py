from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import nltk
from nltk.tokenize import sent_tokenize
from transformers import pipeline, PegasusTokenizer, PegasusForConditionalGeneration, WhisperTokenizer, WhisperFeatureExtractor, WhisperForConditionalGeneration
from moviepy.editor import VideoFileClip

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Download NLTK Data
# -----------------------------
nltk.download("punkt", quiet=True)

# -----------------------------
# Model Paths
# -----------------------------
PEGASUS_PATH = "V:/projects/WhisPeg/models/pegasus_saved"
WHISPER_PATH = "V:/projects/WhisPeg/models/whisper_saved"

# -----------------------------
# Load Pegasus (Summarizer)
# -----------------------------
pegasus_tokenizer = PegasusTokenizer.from_pretrained(PEGASUS_PATH, use_fast=False)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(PEGASUS_PATH)

text_summarizer = pipeline(
    "summarization",
    model=pegasus_model,
    tokenizer=pegasus_tokenizer,
    device=-1
)

# -----------------------------
# Load Whisper (Speech-to-Text)
# -----------------------------
whisper_tokenizer = WhisperTokenizer.from_pretrained(WHISPER_PATH)
whisper_feature_extractor = WhisperFeatureExtractor.from_pretrained(WHISPER_PATH)
whisper_model = WhisperForConditionalGeneration.from_pretrained(WHISPER_PATH)

whisper_pipe = pipeline(
    "automatic-speech-recognition",
    model=whisper_model,
    tokenizer=whisper_tokenizer,
    feature_extractor=whisper_feature_extractor,
    device=-1
)

# -----------------------------
# Chunking Logic
# -----------------------------
def chunk_text(text, max_tokens=900):
    # First, split into sentences (may fail for Whisper)
    sentences = sent_tokenize(text)

    # If Whisper produced 1 giant "sentence", split by phrase length
    if len(sentences) == 1:
        # HARD SPLIT every 40 words to ensure Pegasus safety
        words = text.split()
        sentences = [
            " ".join(words[i:i+40])
            for i in range(0, len(words), 40)
        ]

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in sentences:
        tokens = len(sentence.split())

        # HARD LIMIT: NEVER ALLOW >512 TOKEN CHUNK
        if current_tokens + tokens > 512:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = tokens
            continue

        # NORMAL SPLIT
        if current_tokens + tokens <= max_tokens:
            current_chunk += sentence + " "
            current_tokens += tokens
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
            current_tokens = tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# -----------------------------
# Text Summarization
# -----------------------------
def summarize_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = chunk_text(text)

    chunk_summaries = [
        text_summarizer(chunk, max_length=200, min_length=80, do_sample=False)[0]["summary_text"]
        for chunk in chunks
    ]

    detailed_summary = "\n".join(chunk_summaries)

    short_summary = text_summarizer(
        detailed_summary,
        max_length=80,
        min_length=30,
        do_sample=False
    )[0]["summary_text"]

    return short_summary, detailed_summary

# -----------------------------
# Video Summarization
# -----------------------------
def summarize_video(video_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile("extracted_audio.mp3", verbose=False, logger=None)

    transcription = whisper_pipe("extracted_audio.mp3")
    transcript_text = transcription["text"]

    chunks = chunk_text(transcript_text, max_tokens=900)

    chunk_summaries = [
        text_summarizer(chunk, max_length=200, min_length=80, do_sample=False)[0]["summary_text"]
        for chunk in chunks
    ]

    detailed_summary = "\n".join(chunk_summaries)

    short_summary = text_summarizer(
        detailed_summary,
        max_length=80,
        min_length=30,
        do_sample=False
    )[0]["summary_text"]

    return transcript_text, short_summary, detailed_summary

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/summarize")
async def summarize_file(file: UploadFile = File(...)):

    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    ext = os.path.splitext(file_location)[1].lower()

    if ext == ".txt":
        short_summary, detailed_summary = summarize_text(file_location)
        return {
            "type": "text",
            "transcript": "",
            "short_summary": short_summary,
            "detailed_summary": detailed_summary
        }

    elif ext == ".mp4":
        transcript, short_summary, detailed_summary = summarize_video(file_location)
        return {
            "type": "video",
            "transcript": transcript,
            "short_summary": short_summary,
            "detailed_summary": detailed_summary
        }

    else:
        return {"error": "Unsupported file format. Upload .txt or .mp4."}

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
