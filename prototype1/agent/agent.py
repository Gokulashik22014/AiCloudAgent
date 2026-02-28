from agent.planner_agent import planner_agent
from agent.speak_agent import speak_agent
from agent.deployer_agent import deployer_agent
from google.adk.agents.sequential_agent import SequentialAgent

seq_agent_flow=SequentialAgent(
    name="flow_of_the_agents",
    sub_agents=[planner_agent,deployer_agent]
)
root_agent = seq_agent_flow