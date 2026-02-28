// components/chat/ChatWindow.jsx
import { useState } from "react";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import { sendChatMessage } from "../../utils/ai/chatAgent";

export default function ChatWindow({ projectId }) {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    const userMsg = { role: "user", content: text };
    setMessages(prev => [...prev, userMsg]);

    const aiReply = await sendChatMessage(projectId, text);
    setMessages(prev => [...prev, aiReply]);
  };

//   if (messages.length === 0) {
//     return <p>Start chatting to have your code deployed 🚀</p>;
//   }

  return (
    <div className="chat-bubble">
      {messages.map((m, i) => (
        <ChatMessage key={i} message={m} />
      ))}
      <ChatInput onSend={handleSend} />
    </div>
  );
}
