import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="WhisPeg Summarizer", layout="wide")

st.title("🎙️ WhisPeg – Multimodal Text Summarizer")
st.write("Upload **Text**, **Audio**, or **Video**, and let Pegasus + Whisper generate summaries!")

# Upload Section
uploaded = st.file_uploader("Upload a file (.txt / .mp3 / .wav / .mp4)", type=["txt","mp3","wav","mp4"])

if uploaded:
    file_bytes = uploaded.read()
    files = {"file": (uploaded.name, file_bytes)}

    file_type = uploaded.name.split(".")[-1]

    if file_type == "txt":
        st.info("Summarizing text...")
        response = requests.post(f"{API_URL}/summarize/text", files=files)

    elif file_type in ["mp3", "wav", "mp4"]:
        st.info("Transcribing + Summarizing audio/video...")
        response = requests.post(f"{API_URL}/summarize/audio", files=files)

    else:
        st.error("Unsupported file format.")
        st.stop()

    result = response.json()

    if "transcription" in result:
        st.subheader("📝 Transcription")
        st.write(result["transcription"])

    st.subheader("📌 Summary")
    st.success(result["summary"])
