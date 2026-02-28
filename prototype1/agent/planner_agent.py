from google.adk.agents import Agent,LlmAgent
from google.adk.models.lite_llm import LiteLlm
from agent.tools.planner_tools import check_valid_values,check_terraform,get_current_state,get_desired_state
from google.adk.tools import FunctionTool

ollama_model = LiteLlm(
    model="ollama_chat/llama3.2:1b"
)

planner_agent=LlmAgent(
    model=ollama_model,
    name="planner_agent",
    description="Plans the necessary info about the infra by deciding on the existing state with the help of terraform",
    instruction="""
    You plan the things needed to deploy the instance use the instruction given to understand user needs

    use the tool: get_current_state
        to get the current status of the infra and get a understanding of this and use instruction given to understand what is needed
    use the tool: check_valid_values
        to check if the values you provided are allowed
    use the tool: get_desired_state
        to test if what you came up with is fesible    

    give a json 
    {
        instance_name:"",
        instance_type:"",
        region:"",
    }
    if any of the mentioned is not avaliable then fill them with the allowed values you can come up with

    call get_current_state
    call check_valid_values
    call get_desired_state

""",
    tools=[FunctionTool(get_current_state),FunctionTool(get_desired_state),FunctionTool(check_valid_values)],
    output_key="output_of_planner"
)
