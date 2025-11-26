from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from utils.summarizer import summarize_text
from utils.transcriber import transcribe_audio
from utils.chunker import chunk_text

app = FastAPI(title="WhisPeg – Multimodal Summarizer API")

# Allow Streamlit frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
def health():
    return {"status": "running"}

# ---------------------- TEXT SUMMARIZATION ----------------------
@app.post("/summarize/text")
async def summarize_text_api(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r") as f:
        text = f.read()

    chunks = chunk_text(text)
    summary = summarize_text(chunks)
    return {"summary": summary}

# ---------------------- AUDIO/VIDEO SUMMARIZATION ----------------------
@app.post("/summarize/audio")
async def summarize_audio_api(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcribed_text = transcribe_audio(file_path)
    chunks = chunk_text(transcribed_text)
    summary = summarize_text(chunks)

    return {
        "transcription": transcribed_text,
        "summary": summary
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
