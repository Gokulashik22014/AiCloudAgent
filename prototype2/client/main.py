import os
from dotenv import load_dotenv
from ollama import Client
from api_calls import execute_steps

# import prompts
from prompts import *

load_dotenv()

MODEL = "qwen3.5:cloud"

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_KEY')}
)

# ---------------- STATE ----------------
state = {
    "mode": "chat",         # chat | waiting_confirmation
    "intent": None,
    "last_plan": None,
}

# Persistent conversation history for context carry-over
conversation_history = []


# ---------------- HELPERS ----------------

def detect_intent(user_input):
    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response["message"]["content"]


def get_prompt(intent):
    if "CREATE_INFRA" in intent:
        return CONVERSATION_PROMPT
    elif "UPDATE_INFRA" in intent:
        return CONVERSATION_PROMPT
    elif "ANALYTICS" in intent:
        return ANALYTICS_PROMPT
    return CONVERSATION_PROMPT


def chat_with_history(system_prompt, history):
    """Send a chat request with the full conversation history."""
    messages = [{"role": "system", "content": system_prompt}] + history
    response = client.chat(model=MODEL, messages=messages)
    return response["message"]["content"]


def generate_plan(history):
    """
    Generate a deployment plan using the full conversation history as context,
    so the planner knows everything the user has already described.
    """
    # Summarise the history into a context block for the planner
    context_block = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history
    )
    planner_user_message = (
        "Based on the following conversation, generate a detailed step-by-step "
        "infrastructure deployment plan:\n\n"
        f"{context_block}"
    )

    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": planner_user_message}
        ]
    )
    return response["message"]["content"]


# ---------------- MAIN LOOP ----------------

print("Cloud Infra Chat (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        break

    # ---------------- CONFIRMATION MODE ----------------
    if state["mode"] == "waiting_confirmation":
        if user_input.lower() in ["yes", "y", "confirm"]:
            print("\n🚀 Executing plan...\n")
            execute_steps(state["last_plan"])
            # Reset everything for a fresh session
            state["mode"] = "chat"
            state["last_plan"] = None
            state["intent"] = None
            conversation_history.clear()
        else:
            print("\n❌ Plan discarded. You can continue refining your request.\n")
            state["mode"] = "chat"
            # Keep history intact so the user can adjust and re-deploy
        continue

    # ---------------- DEPLOY TRIGGER ----------------
    # When the user says "deploy" (or similar), skip info-gathering and go straight
    # to the planner using everything collected in the conversation so far.
    if user_input.lower() in ["deploy", "deploy now", "go", "proceed"]:
        if not conversation_history:
            print("\nAgent: Please describe your infrastructure requirements first before deploying.\n")
            continue

        print("\n⚙️  Generating plan from our conversation...\n")
        plan = generate_plan(conversation_history)
        state["last_plan"] = plan

        print("\n📦 Proposed Plan:\n", plan)
        print("\nDo you want to apply this? (yes / no)")
        state["mode"] = "waiting_confirmation"
        continue

    # ---------------- INTENT DETECTION ----------------
    intent = detect_intent(user_input)
    state["intent"] = intent
    print("\n[Intent]:", intent)

    # ---------------- CONVERSATION WITH HISTORY ----------------
    # Add the user's message to history before calling the model
    conversation_history.append({"role": "user", "content": user_input})

    prompt = get_prompt(intent)
    content = chat_with_history(prompt, conversation_history)

    # Add the assistant's reply to history so future turns have full context
    conversation_history.append({"role": "assistant", "content": content})

    print("\nAgent:", content, "\n")