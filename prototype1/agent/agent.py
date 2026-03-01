from agent.planner_agent import planner_agent
from agent.speak_agent import speak_agent
from agent.deployer_agent import deployer_agent
from agent.review_agent import review_agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.loop_agent import LoopAgent


planner_review_loop=LoopAgent(
    name="plan_and_review_loop",
    sub_agents=[planner_agent,review_agent],
    max_iterations=1
)

main_agent_flow=SequentialAgent(
    name="flow_of_the_agents",
    sub_agents=[speak_agent,planner_review_loop,deployer_agent],
)


root_agent = main_agent_flow