import React from "react";
import "./Tabs.css";

function Tabs({ active, setActive }) {
  return (
    <div className="tabs">
      <button
        className={active === "text" ? "tab active" : "tab"}
        onClick={() => setActive("text")}
      >
        Text
      </button>

      <button
        className={active === "audio" ? "tab active" : "tab"}
        onClick={() => setActive("audio")}
      >
        Audio
      </button>

      <button
        className={active === "video" ? "tab active" : "tab"}
        onClick={() => setActive("video")}
      >
        Video
      </button>
    </div>
  );
}

export default Tabs;
