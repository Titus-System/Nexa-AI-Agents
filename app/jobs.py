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
    if data.partnumber == "BC846ALT1G":
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
    print(
        f"Iniciando job para partnumber {data.partnumber} no canal {data.progress_channel}"
    )

    messages = {
        0: "Pedido de análise recebido",
        1: "Iniciando análise de partnumber com agente Nexa-IA",
        2: "Buscando informações técnicas do partnumber",
        3: "Buscando informações técnicas do partnumber",
        4: "Gerando descrição do produto",
        5: "Finalizando descrição do produto"
    }

    try:
        if data.partnumber != "BC846ALT1G":
            redis_publisher.send_failed_processing(data.progress_channel, str(e))

        for i in range(6):
            progress_schema = ProgressSchema(
                current=i, total=5, message=messages.get(i)
            )
            redis_publisher.send_progress_update(data.progress_channel, progress_schema)
            if i < 6: time.sleep(4)
            else: time.sleep(3)

        time.sleep(5)
        result = SingleClassification(
            partnumber=data.partnumber,
            ncm="--",
            description="""transistores de silício NPN de uso geral, apresentados em um invólucro SOT-23. Esses componentes operam com uma corrente de coletor contínua de até 100 mAdc e possuem diferentes classificações de tensão coletor-emissor (VCEO) que variam de 30 V a 65 V, dependendo do modelo específico dentro da série. Projetados para funcionar em uma ampla faixa de temperatura de junção de -55°C a +150°C , eles oferecem uma dissipação de potência total de 225 mW em uma placa FR-5. O ganho de corrente DC (h FE), sob uma tensão de coletor-emissor de 5.0 V e uma corrente de coletor de 2.0 mA, varia entre 110 e 800, dependendo da classificação do componente. A série apresenta um produto de ganho de largura de banda (fT) de no mínimo 100 MHz em uma corrente de coletor de 10 mA.""",
            exception="--",
            nve="--",
            fabricante="onsemi",
            endereco="--",
            pais="--",
            confidence_score=0.95,
        )
        redis_publisher.send_done_classification(data.progress_channel, result)
        return

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, str(e))
    return