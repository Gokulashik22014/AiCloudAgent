// components/chat/ChatMessage.jsx

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div
    className={`chat-message ${isUser ? "user" : "ai"}`}
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "12px",
      }}
    >
      <div
        className="chat-bubble"
        style={{
          maxWidth: "70%",
          padding: "10px 14px",
          borderRadius: "8px",
          backgroundColor: isUser ? "#2563eb" : "#1f2937",
          color: "#fff",
          whiteSpace: "pre-wrap",
          lineHeight: "1.4",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            opacity: 0.7,
            marginBottom: "4px",
          }}
        >
          {isUser ? "You" : "AI"}
        </div>

        <div>{message.content}</div>

        {message.meta?.type === "infra-plan" && (
          <div
            style={{
              marginTop: "8px",
              padding: "8px",
              background: "#111827",
              borderRadius: "6px",
              fontSize: "12px",
            }}
          >
            <strong>Proposed Infrastructure</strong>
            <pre>{JSON.stringify(message.meta.plan, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
