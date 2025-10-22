from smolagents import (
    CodeAgent,
    LiteLLMModel,
    LogLevel,
)
import yaml
from agents.agents.web_search_agent import web_agent
from agents.agents.description_writer_agent import description_agent
from agents.hooks.report import Report
from agents.hooks.logger import log_step_to_file, log_progress
from agents.config import LITELLM_REQUEST_TIMEOUT, OLLAMA_URI
from schemas.api_schemas import SingleClassificationRequest


### TOOLS ---------------------------------------------------------------------------------------------------------


### HOOKS ---------------------------------------------------------------------------------------------------------
# send_progress = report.send_progress
hook_log_progress = log_progress
hook_log_step_to_file = log_step_to_file

report = Report()


### SYSTEM PROMPT  ------------------------------------------------------------------------------------------------
sprompt = "agents/prompts/manager_agent/system_prompt.yaml"  # ~ 2k tokens
with open(sprompt, "r") as stream:
    prompt_templates = yaml.safe_load(stream)


### AGENTS and Models -----------------------------------------------------------------------------------------------

# Check whether the model uses roles (system, assistant, user) in messages. It should use for better performance.

model_id = "ollama/qwen2.5:14b"  # 128K context window
model = LiteLLMModel(
    model_id=model_id,
    api_base=OLLAMA_URI,
    api_key="ollama",
    name="manager",
    max_tokens=12000,
    temperature=0.2,
    timeout=LITELLM_REQUEST_TIMEOUT,
)

## Agent
agent = CodeAgent(
    name="Manager",
    description="Coordinates product specification workflow by managing web search, description writing, and classification agents to transform part numbers into complete product data with technical specs, descriptions, and NCM-EX codes. Provide part number and supplier information as arguments.",
    model=model,
    managed_agents=[
        web_agent,
        description_agent,
    ],
    tools=[],
    additional_authorized_imports=[
        "json",
        "pydantic",
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
        "stat",
    ],
    prompt_templates=prompt_templates,
    max_steps=8,
    verbosity_level=LogLevel.DEBUG,
    return_full_result=True,
    provide_run_summary=True,
    step_callbacks=[
        hook_log_progress,
        hook_log_step_to_file,
    ],
)


### INPUT PROMPT -----------------------------------------------------------------------------------------------
# ~350 tokens
PROMPT_TEMPLATE = """
# Product Specification Processing Task

You are tasked with processing the following product information to generate comprehensive specifications, description, and classification data.

## Input Data

The input data is provided as a Python variable with the following structure:

```python
input_data: dict[str, str] = {
    "part_number": str,      # The exact part number to search for
    "supplier": str,         # Optional The supplier/manufacturer name
    "additional_context": str # Optional additional information (may be empty or absent)
}
```

### Example Structure:
```python
input_data = {
    "part_number": "ABC123",
    "supplier": "TechCorp",
    "additional_context": "Industrial automation component"
}
```

## Your Task

Process the provided input data through your managed agent workflow to produce a complete product specification package. You must coordinate your specialized agents to:

1. Retrieve detailed technical specifications for the given part number from web sources
2. Generate a comprehensive product description based on the retrieved specifications
3. Classify the product with appropriate NCM-EX codes using vector database lookup

## Current Input Data

The specific data you need to process is:

```python
input_data = {
    "part_number": "{{part_number}}",
    "supplier": "{{supplier}}",
    "additional_context": "{{additional_context}}"
}
```

## Expected Output

Return your final response in the required JSON format as specified in your system instructions, containing the processed specifications, description, and classification results.

## Execution Instructions

Begin by analyzing the input data and executing your planned workflow using your managed agents. Follow your established protocols for sequential execution, error handling, and data preservation.
"""


def execute(
    channel: str,
    job_id: str,
    data: SingleClassificationRequest,
    prompt: str | None = None,
) -> str:
    from time import time

    start = time()
    with open("logs/output.log", "a") as file:
        file.write(f"[{start}] Start Running manager.\n")

    report.channel = channel
    report.job_id = job_id

    part_number = data["partnumber"]
    supplier = data["supplier"] or ""
    # additional_context = {
    #     k: v
    #     for k, v in data.items()
    #     if k not in ["partnumber", "supplier", "progress_channel"]
    # }

    if prompt is None:
        prompt = (
            PROMPT_TEMPLATE.replace("{{part_number}}", part_number).replace(
                "{{supplier}}", supplier
            )
            # .replace("{{additional_context}}", str(additional_context))
        )

    ### VISUALIZE THE AGENTS STRUCTURE
    agent.visualize()

    response = agent(prompt)
    report.send_successful_response(response)

    end = time()
    with open("logs/output.log", "a") as file:
        file.write(f"[{end}] Finish Response (manager): {response}\n")
        file.write(f"Duration: {end - start}")

    return response
