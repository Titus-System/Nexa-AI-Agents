from smolagents import (
    CodeAgent,
    LiteLLMModel,
    LogLevel,
)
import yaml
from agents.config import LITELLM_REQUEST_TIMEOUT
from agents.hooks.logger import log_step_to_file, log_progress


### HOOKS ---------------------------------------------------------------------------------------------------------
# send_progress = report.send_progress
hook_log_progress = log_progress
hook_log_step_to_file = log_step_to_file


### SYSTEM PROMPT ------------------------------------------------------------------------------------------------
sprompt = "agents/prompts/description_writer_agent/system_prompt.yaml"  # ~ 2k tokens
with open(sprompt, "r") as stream:
    prompt_templates = yaml.safe_load(stream)


### MODEL ---------------------------------------------------------------------------------------------------------
# Use the same model config style as manager/web agents
# model_id = "ollama/llama3.1:8b"
# model_id = "ollama/qwen2.5:7b"
model_id = "ollama/qwen2.5:14b"

model_desc = LiteLLMModel(
    name="description_writer",
    model_id=model_id,
    api_key="ollama",
    max_tokens=4000,
    temperature=0.5,
    timeout=LITELLM_REQUEST_TIMEOUT,
)

### AGENT ---------------------------------------------------------------------------------------------------------
description_agent = CodeAgent(
    name="description_writer_agent",
    description="Generates clear, engaging, and human-friendly product descriptions in Portuguese based on technical specifications and part numbers.",
    model=model_desc,
    tools=[],
    additional_authorized_imports=[
        "json",
        "re",
        "datetime",
    ],
    prompt_templates=prompt_templates,
    verbosity_level=LogLevel.DEBUG,
    max_steps=3,
    planning_interval=2,
    return_full_result=True,
    step_callbacks=[
        hook_log_progress,
        hook_log_step_to_file,
    ],
)

### PROMPT TEMPLATE -----------------------------------------------------------------------------------------------
PROMPT_TEMPLATE = """
# Product Description Task

You will receive structured input data with:
- part_number: the exact part number of the product
- supplier: the supplier or manufacturer name
- technical_data: dictionary of product specifications (e.g., weight, material, dimensions, power consumption, etc.)
- additional_context: any additional context provided

### Example Structure:
```python
input_data = {
    "part_number": "ABC123",
    "supplier": "TechCorp",
    "technical_data": {
        "weight": "100g",
        "material": "plastic",
        "voltage": "5V"
    },
    "additional_context": "Industrial automation component"
}

## Current Task Data

```python
input_data = {
    "part_number": "{part_number}",
    "supplier": "{supplier}",
    "technical_data": {technical_data},
    "additional_context": "{additional_context}"
}
```

Your goal is to generate a clear, engaging, and human-friendly description in Portuguese.

## Rules
- Write exactly ONE short paragraph (about 1.5-2 lines).
- Do NOT write or execute code. Only produce natural text.
- Do NOT create variables or attempt calculations.
- Use the values exactly as given (e.g., "30W" must stay "30W").
- Mention the part number only once (at the beginning or end).
- Use simple, direct, yet professional language.
- You may omit less relevant details (e.g., color).
- When you find a satisfactory answer, stop processing immediately.
"""


### EXECUTION FUNCTION --------------------------------------------------------------------------------------------
def execute(
    part_number: str,
    supplier: str,
    technical_data: dict | None = None,
    additional_context: str | dict | list | None = None,
    prompt: str | None = None,
) -> str:
    if prompt is None:
        prompt = PROMPT_TEMPLATE.format(
            part_number=part_number,
            supplier=supplier,
            technical_data=technical_data,
            additional_context=additional_context,
        )

    return description_agent.run(prompt)
