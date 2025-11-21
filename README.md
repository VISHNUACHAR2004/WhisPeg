# 🎥 Video and Text Summarizer using Whisper + PEGASUS

## Project Goal
The aim of this project is to **extract meaningful insights from videos** by:
1. Converting audio into text using **speech recognition (Whisper)**.
2. Generating a **concise summary** using transformer-based models like **PEGASUS** or **BART**.

This saves users time by providing quick takeaways from long videos, making it ideal for lectures, podcasts, and meetings.

---

##  Features
- **Automatic Transcription:** Uses [openai/whisper-base](https://huggingface.co/openai/whisper-base) (HuggingFace).
- **Accurate Summarization:** Uses [Pegasus-XSum](https://huggingface.co/google/pegasus-xsum) or default transformers.
- **PDF Export:** Summaries can be downloaded as PDF files.
- **Colab-Friendly:** No local setup required; runs fully in Google Colab (GPU-supported).
- **Noise & Accent Robustness:** Whisper handles multiple languages, accents, and noisy data effectively.
- **Dual Support:** Detects file type (video or text) and applies the correct summarization pipeline.

---

## 🛠 Tech Stack
- **Speech-to-Text (ASR):** HuggingFace `openai/whisper-base`
- **Summarization:** HuggingFace Transformers (Pegasus / BART)
- **Audio Extraction:** `moviepy`
- **PDF Generation:** `fpdf`
- **Notebook Environment:** Google Colab

  ## Whisper Variants
| Variant | Parameters | Speed   | Accuracy       |
|---------|-----------:|---------|---------------:|
| tiny    | 39M        | Very fast | Low accuracy |
| base    | 74M        | Fast     | Good accuracy |
| small   | 244M       | Slower   | Better        |
| medium  | 769M       | Slower   | Great         |
| large   | 1.5B       | Slowest  | Best          |

**I chose `base`** for best speed/accuracy tradeoff on Colab.

---

##  How It Works
1. **Upload a video file** (MP4, etc.).
2. **Extract audio** using `moviepy`.
3. **Transcribe audio** → text using Whisper.
4. **Summarize text** → concise version using PEGASUS/BART.
5. **Export summary** as PDF.

---

## Future Enhancements
- Support for very long videos (automatic chunking)
- Multi-speaker diarization (who said what)
- Real-time transcription & summarization
