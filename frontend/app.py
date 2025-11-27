import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Multimodal Summarizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- DARK MODE CSS ----------
dark_css = """
<style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-color: #0e1117;
    }
    .stTextInput, .stFileUploader {
        background-color: #161a23;
    }
    .stMarkdown, .stTextArea {
        color: white !important;
    }
    .block-container {
        padding-top: 1rem;
    }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center; color:#57a6ff;'>🧠 Multimodal Summarizer (Text + Video)</h1>", unsafe_allow_html=True)
st.markdown("### Upload a **.txt** or **.mp4** file to generate summaries", unsafe_allow_html=True)
st.write("-----")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload File", type=["txt", "mp4"])

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("Process File"):
        with st.spinner("Processing... Please wait ⏳"):

            # Send file to FastAPI
            files = {"file": uploaded_file.getvalue()}
            filename = uploaded_file.name

            res = requests.post(
                "http://localhost:8000/summarize",
                files={"file": (filename, uploaded_file, uploaded_file.type)}
            )

            if res.status_code == 200:
                output = res.json()

                file_type = output.get("type")

                st.write("## 📌 Output")

                if file_type == "text":
                    st.markdown("### 📝 Short Summary")
                    st.info(output["short_summary"])

                    st.markdown("### 📄 Detailed Summary")
                    st.success(output["detailed_summary"])

                elif file_type == "video":
                    st.markdown("### 🎤 Transcript")
                    st.code(output["transcript"], language="text")

                    st.markdown("### 📝 Summary")
                    st.success(output["short_summary"])

                else:
                    st.error("Unknown response type.")

            else:
                st.error("Something went wrong with the backend!")
