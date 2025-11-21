import React, { useState } from "react";
import axios from "axios";

function VideoSummarizer() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [transcription, setTranscription] = useState("");

  const submitVideo = async () => {
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    const res = await axios.post("http://localhost:8000/summarize/video", form);

    setTranscription(res.data.transcription);
    setSummary(res.data.summary);
  };

  return (
    <div className="card">
      <h2>Video Summarizer</h2>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="file-input"
      />

      <button className="btn" onClick={submitVideo}>
        Summarize Video
      </button>

      {transcription && (
        <div className="result">
          <h3>Transcription:</h3>
          <p>{transcription}</p>

          <h3>Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default VideoSummarizer;
