from smolagents import (
    CodeAgent,
    LiteLLMModel,
    LogLevel,
    # EMPTY_PROMPT_TEMPLATES,
    # PromptTemplates,
)
import yaml
from agents.agents.web_search_agent import web_agent
from agents.agents.description_writer_agent import description_agent
from agents.agents.classificator_agent import classificator_agent
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

# # Load the smolagents Empty Prompt Template
# prompt_templates: PromptTemplates = EMPTY_PROMPT_TEMPLATES


### AGENTS and Models -----------------------------------------------------------------------------------------------

# Check whether the model uses roles (system, assistant, user) in messages. It should use for better performance.
model_id = "ollama/llama3.1:8b"
model_id = "ollama/qwen2.5:7b"
model_id = "ollama/qwen2.5:14b"  # 128K context window
model = LiteLLMModel(
    model_id=model_id,
    api_base=OLLAMA_URI,
    api_key="ollama",
    name="manager",
    max_tokens=12000,  # maximum output length you want the model to generate.
    temperature=0.2,  #
    # top_k= ,  # Model considers only the top K most likely tokens at each step. 1 to model's number of tokens. Creative writing (top_k=50+), deterministic output (top_k=1).
    # top_p= ,  # Model considers only the *smallest* set of tokens whose cumulative probability ≥ p. Range: 0.0 → 1.0. So, 1.0 will consider all the set of tokens, and 0.5 will consider the smallest set containing all the highest-probability tokens whose cumulative probability >= 0.5.
    # flatten_messages_as_text=False,  # Flattens structured message objects to plain text in some cases. I.e. combining them rather than preserving role/message-structure.
    # custom_role_conversions=None, # mapping to convert message roles. For example, if a model doesn’t understand role “system” or “assistant”, you can remap them. This lets you map messages roles appropriately so that prompts are interpreted correctly.
    # repeat_penalty=1.1, # Penalizes tokens that were already used in the context window. 1.0 = stronger penalty (less repetition).
    # presence_penalty= , # discourages repeating ideas already mentioned (helps encourage new topics). Positive values = more novelty.
    # frequency_penalty= , #
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
        classificator_agent,
    ],
    tools=[
        # uses final_answer internally
    ],
    additional_authorized_imports=[
        # libraries the agent is allowed to use
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
    prompt_templates=prompt_templates,  # Determines how instructions / tools / structure are presented to the LLM.
    # instructions= ,   # Custom instructions string to be injected in the system prompt. Helps guide behavior (tell it what goals are, constraints, style).
    max_steps=8,  # Maximum number of steps (ReAct cycle) the agent can take (Thought -> Act -> Observation). Avoid infinity loops.
    # planning_interval=7,  # Planning steps allow the agent to review what has been done / what remains, perhaps adjust its next steps, which can be useful for more complex tasks. Trade off: consumes one step of `max_steps`.
    verbosity_level=LogLevel.DEBUG,  # or OFF, ERROR, INFO, DEBUG
    return_full_result=True,  # Whether it should return the full result object (including intermediate thoughts, code, observations). Useful for debug.
    # code_block_tags=("<code>", "</code>"),
    provide_run_summary=True,  # Whether to provide a run summary when called as a managed agent.
    # grammar=None,
    step_callbacks=[
        hook_log_progress,
        hook_log_step_to_file,
    ],  # Functions / hooks that get called at each step or associated with memory steps. For monitoring/tracing or custom behavior.
    # final_answer_checks=[],  # A list of callable checks which, just before accepting a final answer, run validations on the answer. If any fails, the agent might try again or indicate failure.
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
