import logging
from smolagents import MemoryStep

path = "logs"


# Configure logging
logging.basicConfig(
    filename=f"{path}/agent_progress.log",
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
)


def log_progress(memory_step: MemoryStep, agent=None):
    agent_name = agent.name if agent else ""
    with open(f"{path}/output_{agent_name}_agent.log", "a") as file:
        file.write("ITERATION ============================\n")
        file.write("MEMORY STEP: -------------------------\n")
        # Write all attributes of the memory_step object
        for attr_name in dir(memory_step):
            if not attr_name.startswith("_"):  # Skip private attributes
                attr_value = getattr(memory_step, attr_name)
                file.write(f"{attr_name}: {attr_value}\n")

        file.write("AGENT: -------------------------------\n")
        if agent is not None:
            for attr_name in dir(agent):
                if not attr_name.startswith("_"):
                    attr_value = getattr(agent, attr_name)
                    file.write(f"{attr_name}: {attr_value}\n")


def log_step_to_file(memory_step: MemoryStep, agent=None):
    logging.info(f"Step #{memory_step.step_number} completed.")
    if hasattr(memory_step, "thoughts"):
        logging.info(f"Thoughts: {memory_step.thoughts}")
    if hasattr(memory_step, "code"):
        logging.info(f"Code executed:\n{memory_step.code}")
    if hasattr(memory_step, "observation"):
        logging.info(f"Observation: {memory_step.observation}")
