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
    "mode": "chat",   # chat | waiting_confirmation
    "intent": None,
    "last_plan": None
}

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


def generate_plan(user_input):
    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response["message"]["content"]


# ---------------- MAIN LOOP ----------------

print("Cloud Infra Chat (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # ---------------- CONFIRMATION MODE ----------------
    if state["mode"] == "waiting_confirmation":
        if user_input.lower() in ["yes", "y", "confirm"]:
            print("\n🚀 Executing plan...\n")
            execute_steps(state["last_plan"])
            state["mode"] = "chat"
            state["last_plan"] = None
        else:
            print("\n❌ Plan discarded. Modify your request.\n")
            state["mode"] = "chat"
        continue

    # ---------------- INTENT DETECTION ----------------
    intent = detect_intent(user_input)
    state["intent"] = intent

    print("\n[Intent]:", intent)

    # ---------------- CONVERSATION ----------------
    prompt = get_prompt(intent)

    convo_response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    content = convo_response["message"]["content"]
    print("\nAgent:", content)

    # ---------------- READY TO PLAN ----------------
    if "READY_TO_PLAN" in content:
        print("\n⚙️ Generating plan...\n")

        plan = generate_plan(user_input)

        state["last_plan"] = plan

        print("\n📦 Proposed Plan:\n", plan)
        print("\nDo you want to apply this? (yes/no)")

        state["mode"] = "waiting_confirmation"