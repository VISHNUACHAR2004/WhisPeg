from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os
import uuid
import moviepy.editor as mp
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI(title="WhisPeg API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load Pegasus Model
# -----------------------------
PEGASUS_MODEL_DIR = "models/pegasus_model"
pegasus_tokenizer = AutoTokenizer.from_pretrained(PEGASUS_MODEL_DIR)
pegasus_model = AutoModelForSeq2SeqLM.from_pretrained(PEGASUS_MODEL_DIR)

pegasus_pipe = pipeline(
    "summarization",
    model=pegasus_model,
    tokenizer=pegasus_tokenizer,
    framework="pt",
    device=0 if torch.cuda.is_available() else -1
)

# -----------------------------
# Load Whisper Base Model
# -----------------------------
WHISPER_DIR = "models/whisper_model"

whisper_pipe = pipeline(
    "automatic-speech-recognition",
    model=WHISPER_DIR,
    tokenizer=WHISPER_DIR,
    feature_extractor=WHISPER_DIR
)

# -----------------------------
# Utility: Chunk Long Text
# -----------------------------
def chunk_text(text, max_tokens=900):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= max_tokens:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks

# -----------------------------
# TEXT SUMMARIZATION ENDPOINT
# -----------------------------
class TextRequest(BaseModel):
    text: str

@app.post("/summarize/text")
def summarize_text(req: TextRequest):

    chunks = chunk_text(req.text)
    summaries = []

    for chunk in chunks:
        sm = pegasus_pipe(chunk, max_length=80, min_length=20)
        summaries.append(sm[0]["summary_text"])

    final_summary = " ".join(summaries)
    return {"summary": final_summary}

# -----------------------------
# AUDIO SUMMARIZATION ENDPOINT
# -----------------------------
@app.post("/summarize/audio")
async def summarize_audio(file: UploadFile = File(...)):

    temp_path = f"uploads/{uuid.uuid4()}.mp3"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcription = whisper_pipe(temp_path)
    text = transcription["text"]

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        sm = pegasus_pipe(chunk)
        summaries.append(sm[0]["summary_text"])

    final_summary = " ".join(summaries)
    os.remove(temp_path)

    return {
        "transcription": text,
        "summary": final_summary
    }

# -----------------------------
# VIDEO SUMMARIZATION ENDPOINT
# -----------------------------
@app.post("/summarize/video")
async def summarize_video(file: UploadFile = File(...)):

    video_path = f"uploads/{uuid.uuid4()}.mp4"
    audio_path = video_path.replace(".mp4", ".mp3")

    # Save video
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract audio
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    # Whisper transcription
    transcription = whisper_pipe(audio_path)
    text = transcription["text"]

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        sm = pegasus_pipe(chunk)
        summaries.append(sm[0]["summary_text"])

    final_summary = " ".join(summaries)

    # Clean up
    os.remove(video_path)
    os.remove(audio_path)

    return {
        "transcription": text,
        "summary": final_summary
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "WhisPeg backend running!"}


#syntax to run: uvicorn backend.main:app --host
