// components/chat/ChatInput.jsx
import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  return (
    <div className="chat-input-container">
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Describe what you want to deploy..."
      />
      <button
        onClick={() => {
          onSend(text);
          setText("");
        }}
      >
        Send
      </button>
    </div>
  );
}
