from smolagents import (
    CodeAgent,
    LiteLLMModel,
    LogLevel,
)
import yaml
from agents import web_search_agent


### TOOLS ---------------------------------------------------------------------------------------------------------


### AGENTS and LLMs -----------------------------------------------------------------------------------------------

model_id = "ollama/llama3.1:8b"
model = LiteLLMModel(
    model_id=model_id,
    api_key="ollama",
    name="manager",
    max_tokens=2096,
    temperature=0.2,
)

agent = CodeAgent(
    name="Manager",
    description="Manages and coordinates specialized agents to generate a complete ebook from a user prompt.",
    model=model,
    managed_agents=[
        web_search_agent,
    ],
    tools=[],
    additional_authorized_imports=[
        "random",
        "math",
        "unicodedata",
        "statistics",
        "time",
        "re",
        "datetime",
        "collections",
        "itertools",
        "queue",
    ],
    max_steps=10,
    planning_interval=7,
    verbosity_level=LogLevel.DEBUG,
    return_full_result=True,
)


### VISUALIZE THE AGENTS STRUCTURE
agent.visualize()

input_prompt = ""

### EXECUTE AGENT -----------------------------------------------------------------------------------------------
# agent.run("")
response = agent(input_prompt)
