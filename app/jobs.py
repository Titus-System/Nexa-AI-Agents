import time

from app.simul import run_batch_simul, run_single_simul
from schemas.api_schemas import (
    BatchClassificationRequest,
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
    from .simul import pre_proc
    if data.partnumber in pre_proc.keys():
        run_demo(data, job_id)
        return
    
    try:
        # for i in range(3):
        #     time.sleep(1)
        #     progress_schema = ProgressSchema(
        #         current=i + 1, total=3, message="Analisando dados no servidor Nexa-IA"
        #     )
        #     redis_publisher.send_progress_update(data.progress_channel, progress_schema)

        # call manager agent

        progress_schema = ProgressSchema(
            current=1, total=5, message="Analisando dados no servidor Nexa-IA"
        )
        redis_publisher.send_progress_update(data.progress_channel, progress_schema)
        manager_agent(channel=data.progress_channel, job_id=job_id, data=data)

        # time.sleep(1)
        # result = SingleClassification(
        #     partnumber=data.partnumber,
        #     ncm="123456788",
        #     description="Descrição detalhada do produto",
        #     exception="01",
        #     nve="01",
        #     fabricante="fábrica Nexa",
        #     endereco="av pequim",
        #     pais="China",
        #     confidence_score=0.98,
        # )
        # redis_publisher.send_done_classification(data.progress_channel, result)
        return

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, str(e))



def run_demo(data: SingleClassificationRequest, job_id: str):
    run_single_simul(data, job_id)


def start_batch_classification_job(data: BatchClassificationRequest, job_id: str):
    run_batch_simul(data, job_id)