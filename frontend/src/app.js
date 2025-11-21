import React, { useState } from "react";
import Tabs from "./components/Tabs";
import TextSummarizer from "./components/TextSummarizer";
import AudioSummarizer from "./components/AudioSummarizer";
import VideoSummarizer from "./components/VideoSummarizer";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("text");

  return (
    <div className="app">
      <h1 className="title">WhisPeg – Multimodal Summarizer</h1>

      <Tabs active={activeTab} setActive={setActiveTab} />

      <div className="content">
        {activeTab === "text" && <TextSummarizer />}
        {activeTab === "audio" && <AudioSummarizer />}
        {activeTab === "video" && <VideoSummarizer />}
      </div>
    </div>
  );
}

export default App;
