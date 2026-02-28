// utils/ai/chatAgent.js
export async function sendChatMessage(projectId, message) {
  // call backend → LLM → agent orchestration
  return {
    role: "assistant",
    content: "I will need cloud region, traffic, and database choice."
  };
}
