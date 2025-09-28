import time

from schemas.api_schemas import (
    ProgressSchema,
    SingleClassification,
    SingleClassificationRequest,
)
from .extensions import redis_publisher
from agents.app import manager_agent


def start_single_classification_job(data: SingleClassificationRequest, job_id: str):
    print(
        f"Iniciando job para partnumber {data.partnumber} no canal {data.progress_channel}"
    )
    try:
        for i in range(3):
            time.sleep(1)
            progress_schema = ProgressSchema(
                current=i + 1, total=3, message="Analisando dados no servidor Nexa-IA"
            )
            redis_publisher.send_progress_update(
                data.progress_channel, job_id, progress_schema
            )

            # call manager agent
            manager_agent(channel=data.progress_channel, job_id=job_id, data=data)

        time.sleep(1)
        result = SingleClassification(
            partnumber=data.partnumber,
            ncm="123456788",
            description="Descrição detalhada do produto",
            exception="01",
            nve="01",
            fabricante="fábrica Nexa",
            endereco="av pequim",
            pais="China",
            confidence_score=0.98,
        )
        redis_publisher.send_done_classification(data.progress_channel, job_id, result)
        return

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, job_id, str(e))
