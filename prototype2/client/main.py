import ollama
from ollama import Client
from dotenv import load_dotenv
import os
from api_calls import execute_steps
load_dotenv()


MODEL = "qwen3.5:cloud"

print("Cloud Infra Chat (type 'exit' to quit)\n")

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_KEY')}
)

PROMPT="""
You are a cloud infrastructure planning assistant.

Your task is to convert the user's request into a sequence of API calls for a Terraform automation server.

AVAILABLE ROUTES

GET /terraform/init
    -does not need a input
    -the function is used for the initialization of the terraform
GET /terraform/state
    -does not need a input
    -the function is used to get the current state of the terraform
    -call it if you need to know the existing state to decide on the next things to be added
POST /terraform/plan
    -takes input
    -the function is used to plan the infra
    -use if you want to check the new state with the users asked and for comparing with the current state if needed
POST /terraform/apply
    -takes input as plan name tfplan
POST /addresource
    -takes input only ec2 or s3
    -use it if necessary
    -used to add a template to existing terraform file so the only options avaliable are ec2 and s3

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

OUTPUT:
{
  "steps":[
    {
        "step":1,
        "route":<method> <specify based on workflow>,
        "input":{
            <specify for the step only if it is necessary>
        }
    }
  ]
}

provide only the json as the ouput no need of anything else
"""


messages=[
    {
        "role": "system",
        "content": PROMPT
    },
            
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = ""

    for part in client.chat(model=MODEL, messages=messages, stream=True):
        content = part["message"]["content"]
        print(content, end="", flush=True)
        response += content
    execute_steps(response)
    print()

    messages.append({
        "role": "assistant",
        "content": response
    })