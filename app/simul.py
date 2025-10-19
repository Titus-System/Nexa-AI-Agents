import time
from schemas.api_schemas import (
    BatchClassificationRequest,
    ProgressSchema,
    SingleClassification,
    SingleClassificationRequest,
)
from .extensions import redis_publisher


pre_proc = {
    "BC846ALT1G": SingleClassification(
        partnumber="BC846ALT1G",
        ncm="85412120",
        description="""transistores de silício NPN de uso geral, apresentados em um invólucro SOT-23. Esses componentes operam com uma corrente de coletor contínua de até 100 mAdc e possuem diferentes classificações de tensão coletor-emissor (VCEO) que variam de 30 V a 65 V, dependendo do modelo específico dentro da série. Projetados para funcionar em uma ampla faixa de temperatura de junção de -55°C a +150°C , eles oferecem uma dissipação de potência total de 225 mW em uma placa FR-5. O ganho de corrente DC (h FE), sob uma tensão de coletor-emissor de 5.0 V e uma corrente de coletor de 2.0 mA, varia entre 110 e 800, dependendo da classificação do componente. A série apresenta um produto de ganho de largura de banda (fT) de no mínimo 100 MHz em uma corrente de coletor de 10 mA.""",
        exception="00",
        nve="--",
        fabricante="ONSEMI",
        endereco="5701 North Pima Road, Scottsdale, Arizona, 85250, EUA",
        pais="CHINA, REPUBLICA POPULAR",
        confidence_score=0.95,
    ),
    "88512006119": SingleClassification(
        partnumber="88512006119",
        ncm="85322410",
        description="""capacitor cerâmico multicamadas (MLCC) da série WCAP-CSGP. É um componente de uso geral projetado para uma ampla variedade de aplicações, como acoplamento, desacoplamento e filtragem. As principais características técnicas da série incluem uma vasta gama de encapsulamentos para montagem em superfície (de 0201 a 2220), tensões nominais de 6.3V a 100V e valores de capacitância de 0.5 pF a 100 µF. Utiliza dielétricos de alta performance como NP0 (Classe I), X7R e X5R (Classe II), e opera numa faixa de temperatura de -55 °C a +125 °C.""",
        exception="00",
        nve="--",
        fabricante="Würth Elektronik".upper(),
        endereco="Max-Eyth-Straße 1, 74638 Waldenburg".upper(),
        pais="ALEMANHA",
        confidence_score=0.95,
    )
}

messages = {
    0: "Pedido de análise recebido",
    1: "Iniciando análise de partnumber com agente Nexa-IA",
    2: "Buscando informações técnicas do partnumber",
    3: "Buscando informações técnicas do partnumber",
    4: "Gerando descrição do produto",
    5: "Finalizando descrição do produto"
}

def run_single_simul(data: SingleClassificationRequest, job_id: str):
    print(f"Iniciando job para partnumber {data.partnumber} no canal {data.progress_channel}")

    try:
        if data.partnumber not in pre_proc.keys():
            redis_publisher.send_failed_processing(data.progress_channel, str(e))

        for i in range(6):
            progress_schema = ProgressSchema(
                current=i, total=5, message=messages.get(i)
            )
            redis_publisher.send_progress_update(data.progress_channel, progress_schema)
            if i < 6: time.sleep(4)
            else: time.sleep(3)

        time.sleep(5)
        result = pre_proc[data.partnumber]
        redis_publisher.send_done_classification(data.progress_channel, result, job_id)
        return result

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, str(e))
    return


def run_batch_simul(data: BatchClassificationRequest, job_id: str):
    print(f"Iniciando job para classificação dos partnumbers: {data.partnumbers} no canal {data.progress_channel}")
    total = len(data.partnumbers)
    for i in range(total):
        p = data.partnumbers[i]
        try:
            redis_publisher.send_progress_update(
                data.progress_channel,
                ProgressSchema(current=i, total=total, message=f"[{i}] Processando partnumber {p} com Nexa IA")
            )
            result = pre_proc.get(p, None)
            if result is not None:
                redis_publisher.send_partial_result(
                    channel = data.progress_channel,
                    job_id = job_id,
                    result = result,
                    current = i,
                    total = total,
                    message = f"Classificação encontrada para o partnumber {p}"
                )
        except Exception as e:
            print(f"Erro ao processar classificação do partnumber {p}")
            pass
    redis_publisher.send_done_job(channel=data.progress_channel, job_id=job_id)
    return
