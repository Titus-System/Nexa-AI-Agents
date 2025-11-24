from flask import json
import redis

from schemas.api_schemas import DoneProcessing, FailedProcessing, PartialResult, ProgressSchema, SingleClassification, UpdateProgressStatus
from .config import settings


redis_client = redis.from_url(settings.REDIS_URL)


class RedisPublisher:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client


    def send_progress_update(self, channel: str, progress: ProgressSchema, job_id:str = None):
        print(f"Enviando atualização de progresso para o canal {channel}")
        update = UpdateProgressStatus(
            status='processing',
            job_id= job_id,
            progress=progress
        )
        self.redis_client.publish(channel, json.dumps(update.model_dump()))


    def send_partial_result(self, channel:str, result: SingleClassification | str, job_id:str, current:int, total:int, message:str):
        print(f"Enviando resultado parcial para o canal {channel}")
        payload = PartialResult(
            status = "partial_result",
            job_id = job_id,
            current = current, 
            total = total,
            message = message,
            single_classification=result
        )
        self.redis_client.publish(channel, json.dumps(payload.model_dump()))
        pass

    def send_done_job(self, channel:str, job_id:str):
        payload = {
            "status": "done",
            "job_id": job_id
        }
        self.redis_client.publish(channel, json.dumps(payload))


    def send_done_classification(self, channel:str, result:SingleClassification, job_id:str = None):
        print(f"Enviando resultado final para o canal {channel}")
        done_processing = DoneProcessing(
            status='done',
            job_id= job_id,
            result = result
        )
        self.redis_client.publish(channel, json.dumps(done_processing.model_dump()))


    def send_failed_processing(self, channel:str, error:str, job_id:str = None):
        print(f"Enviando falha de processamento para o canal {channel}")
        failed_processing = FailedProcessing(
            status = 'failed',
            job_id= job_id,
            error = error
        ) 
        self.redis_client.publish(channel, json.dumps(failed_processing.model_dump()))


redis_publisher = RedisPublisher(redis_client)