from google.adk.agents import Agent,LlmAgent
from google.adk.models.lite_llm import LiteLlm

ollama_model = LiteLlm(
    model="ollama_chat/llama3.2:1b"
)

google_model='gemini-2.5-flash'

speak_agent = LlmAgent(
    model=ollama_model,
    name="speak_agent",
    description="Orchestrates infrastructure agents and manages user interaction",
    instruction="""
You are the root orchestration agent.

Responsibilities:

1. Receive infrastructure requests from the user.
2. Translate the request into a structured infrastructure task.
3. Delegate ALL Terraform-related planning and execution to planner_agent.
4. Do NOT attempt to call Terraform tools yourself.
5. Wait for planner_agent to complete execution.
6. Return planner_agent's final result directly to the user.
7. If planner_agent returns an error, clearly report the error.
8. Do not modify or fabricate Terraform results.

Communication Policy:
- Always forward infrastructure tasks to planner_agent.
- Always return planner_agent's final structured response.

Finally give output as
{
       "instance_type",
       "region",
        "instance_name",
}
 with the user specified values if user has not specified anything about the service give it as null
""",
output_key="output_of_speaker"
)

