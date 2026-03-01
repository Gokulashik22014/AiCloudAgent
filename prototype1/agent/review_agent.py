from google.adk.agents import Agent,LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool
from agent.tools.review_tools import check_valid_values
ollama_model = LiteLlm(
    model="ollama_chat/llama3.2:1b"
)
google_model='gemini-2.5-flash'
review_agent=LlmAgent(
    model=ollama_model,
    name="review_agent",
    description="Review the infra that is been provided by the planner agent",
    instruction="""
    You are a review agent who will be reviewing the infra plan of {output_of_planner} evaluate the details based on the tool check_valid_values

    call the tool and generate the response based on that 
""",
    tools=[FunctionTool(check_valid_values)],
    output_key="output_of_review"
)
