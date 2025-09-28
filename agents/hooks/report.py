from smolagents import MemoryStep
from app.extensions import redis_publisher
from schemas.api_schemas import ProgressSchema, SingleClassification


class Report:

    def __init__(self, channel: str = None, job_id: str = None):
        self.channel = channel
        self.job_id = job_id

    def send_progress(self, memory_step: MemoryStep, agent=None):
        """
        Send the agent progress to the API.
        """
        progress: ProgressSchema = {
            "current": memory_step.step_number,
            "total": agent.max_steps if agent else -1,
            "message": memory_step.model_output,
        }
        redis_publisher.send_progress_update(
            self.channel,
            self.job_id,
            progress,
        )

    def send_successful_response(self, response: str):
        """
        Send the agent response to the API.
        """
        result: SingleClassification = {"description": response}
        redis_publisher.send_done_classification(self.channel, self.job_id, result)
