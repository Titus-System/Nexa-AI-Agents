from smolagents import (
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    LogLevel,
    PythonInterpreterTool,
)
import yaml
from agents.config import LITELLM_REQUEST_TIMEOUT
from agents.tools.search_wikipedia import SearchWikipedia
from agents.prompts.web_search_agent.manufacturers import (
    SEARCH_ADDRESSES,
    SITE_ADDRESSES,
)
from agents.hooks.logger import log_step_to_file, log_progress


### TOOLS ---------------------------------------------------------------------------------------------------------
duckduckgo = DuckDuckGoSearchTool()
visit_page = VisitWebpageTool()
wikipedia = SearchWikipedia()


### HOOKS ---------------------------------------------------------------------------------------------------------
# send_progress = report.send_progress
hook_log_progress = log_progress
hook_log_step_to_file = log_step_to_file


### SYSTEM PROMPT  ------------------------------------------------------------------------------------------------
sprompt = "agents/prompts/web_search_agent/system_prompt.yaml"  # ~ 2k tokens
with open(sprompt, "r") as stream:
    prompt_templates = yaml.safe_load(stream)

# Replace the manufacturer's sites placeholders
prompt_templates["system_prompt"] = (
    prompt_templates["system_prompt"]
    .replace("{{manufacturer_sites}}", str(list(SITE_ADDRESSES.values())).strip("[]"))
    .replace("{{direct_search_urls}}", str(list(SEARCH_ADDRESSES.values())).strip("[]"))
)


### AGENTS and Models -----------------------------------------------------------------------------------------------
model_id = "ollama/llama3.1:8b"
model_id = "ollama/qwen2.5:7b"
model_id = "ollama/qwen2.5:14b"
model_web = LiteLLMModel(
    name="web_search",
    model_id=model_id,
    api_key="ollama",
    max_tokens=12000,
    temperature=0.8,
    timeout=LITELLM_REQUEST_TIMEOUT,
)

web_agent = CodeAgent(
    name="web_search_agent",
    description="Finds and extracts comprehensive technical specifications for product part numbers from manufacturer and distributor websites. Provide part number and supplier information as arguments.",
    model=model_web,
    tools=[
        duckduckgo,
        visit_page,
        wikipedia,
        PythonInterpreterTool(additional_authorized_imports=["bs4", "lxml"]),
    ],
    additional_authorized_imports=[
        "bs4",
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
        "requests",
    ],
    prompt_templates=prompt_templates,
    verbosity_level=LogLevel.DEBUG,
    max_steps=6,
    # grammar=None,
    planning_interval=4,
    return_full_result=True,  # Whether it should return the full result object (including intermediate thoughts, code, observations). Useful for debug.
    step_callbacks=[
        hook_log_progress,
        hook_log_step_to_file,
    ],
)


PROMPT_TEMPLATE = """
# Technical Specification Search Task

Find and extract comprehensive technical specifications for the provided part number.

## Input Data Structure

```python
input_data: dict[str, str] = {
    "part_number": str,         # The exact part number to search for
    "supplier": str,           # The supplier/manufacturer name (may be empty)
    "additional_context": str  # Optional additional information (may be empty or absent)
}
```

### Example:
```python
input_data = {
    "part_number": "ABC123",
    "supplier": "TechCorp",
    "additional_context": "Industrial automation component"
}
```

## Current Task Data

```python
input_data = {
    "part_number": "{part_number}",
    "supplier": "{supplier}",
    "additional_context": "{additional_context}"
}
```

## Task Objective

Extract all available technical specifications for this part number and return them in the required JSON format, or provide a detailed failure explanation if unsuccessful.

Begin your search process.
"""


def execute(
    part_number: str,
    supplier: str,
    additional_context: str | dict | list | None = None,
    prompt: str | None = None,
) -> str:
    if prompt is None:
        prompt = PROMPT_TEMPLATE.format(
            part_number=part_number,
            supplier=supplier,
            additional_context=additional_context,
        )

    return web_agent.run(prompt)
