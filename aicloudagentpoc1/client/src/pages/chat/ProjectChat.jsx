// pages/chat/ProjectChat.jsx
import { useParams } from "react-router-dom";
import ChatWindow from "../../components/chat/ChatWindow";
import MetricsPanel from "../../components/metrics/MetricsPanel";

export default function ProjectChat() {
  const { projectId } = useParams();

  return (
    <div className="project-chat-layout">
      <aside className="metrics-section">
        <MetricsPanel projectId={projectId} />
      </aside>

      <main className="chat-section">
        <ChatWindow projectId={projectId} />
      </main>
    </div>
  );
}
