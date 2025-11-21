import React, { useState } from "react";
import axios from "axios";

function TextSummarizer() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");

  const summarize = async () => {
    if (!text.trim()) return;

    const res = await axios.post("http://localhost:8000/summarize/text", {
      text: text,
    });

    setSummary(res.data.summary);
  };

  return (
    <div className="card">
      <h2>Text Summarizer</h2>

      <textarea
        className="input-box"
        placeholder="Paste long text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button className="btn" onClick={summarize}>
        Summarize
      </button>

      {summary && (
        <div className="result">
          <h3>Summary:</h3>
          <p>{summary}</p>
        </div>
      )}
    </div>
  );
}

export default TextSummarizer;
