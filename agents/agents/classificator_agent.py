from smolagents import (
    CodeAgent,
    LiteLLMModel,
    LogLevel,
)
import yaml
from agents.config import LITELLM_REQUEST_TIMEOUT, OLLAMA_URI
from agents.hooks.logger import log_step_to_file, log_progress
from agents.tools.query_rag import query_chroma

### TOOLS ---------------------------------------------------------------------------------------------------------
chroma = query_chroma

### HOOKS ---------------------------------------------------------------------------------------------------------
# send_progress = report.send_progress
hook_log_progress = log_progress
hook_log_step_to_file = log_step_to_file


### SYSTEM PROMPT  ------------------------------------------------------------------------------------------------
sprompt = "agents/prompts/classificator_agent/system_prompt.yaml"
with open(sprompt, "r") as stream:
    prompt_templates = yaml.safe_load(stream)


### AGENTS and Models -----------------------------------------------------------------------------------------------
model_id = "ollama/qwen2.5:14b"
# model_id = "ollama/qwen3:8b"
model_classificator = LiteLLMModel(
    name="classificator",
    model_id=model_id,
    api_key="ollama",
    api_base=OLLAMA_URI,
    max_tokens=12000,
    temperature=0.3,
    timeout=LITELLM_REQUEST_TIMEOUT,
)

classificator_agent = CodeAgent(
    name="classificator_agent",
    description="Retrieves NCM (Nomenclatura Comum do Mercosul) classification codes and bilingual product descriptions by querying a Chroma vector database using English technical specifications as input.",
    model=model_classificator,
    tools=[chroma],
    additional_authorized_imports=[
        "json",
        "pydantic",
        "collections",
        "itertools",
        "queue",
        "math",
        "datetime",
        "stat",
        "random",
        "re",
        "unicodedata",
        "time",
        "statistics",
    ],
    prompt_templates=prompt_templates,
    verbosity_level=LogLevel.DEBUG,
    max_steps=5,
    planning_interval=3,
    return_full_result=True,
    step_callbacks=[
        hook_log_progress,
        hook_log_step_to_file,
    ],
)

PROMPT_TEMPLATE = """
Find the most relevant NCM (Nomenclatura Comum do Mercosul) and EX codes for the following product:

Product specifications: {{product_specs}}
"""


def execute(
    product_specs: str,
    prompt: str | None = None,
) -> str:
    if prompt is None:
        prompt = PROMPT_TEMPLATE.replace("{{product_specs}}", product_specs)

    return classificator_agent.run(prompt)
