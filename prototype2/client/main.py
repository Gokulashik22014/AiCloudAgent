import ollama

MODEL = "llama3.2:1b"

print("Cloud Infra Chat (type 'exit' to quit)\n")
PROMPT="""
You are a cloud infrastructure planning assistant.

Your task is to convert the user's request into a sequence of API calls for a Terraform automation server.

AVAILABLE ROUTES

GET /terraform/init
GET /terraform/state
POST /terraform/plan
POST /terraform/apply
POST /addresource

AVAILABLE VARIABLES

region
instance_type
ami
instance_name

DEFAULT VALUES
region = ap-south-1
instance_type = t2.micro
ami = ami-123456
instance_name = terraform-instance

WORKFLOW
1. /terraform/init
2. /addresource
3. /terraform/plan
4. /terraform/apply

Return JSON only.

Format:

{
  "step_1": {
    "route": "...",
    "input": {}
  }
}
"""
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("AI:", response["message"]["content"])