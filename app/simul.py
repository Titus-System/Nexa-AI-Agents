import time
from schemas.api_schemas import (
    BatchClassificationRequest,
    ProgressSchema,
    SingleClassification,
    SingleClassificationRequest,
)
from .extensions import redis_publisher
from app.pre_proc import pre_proc


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
            redis_publisher.send_failed_processing(data.progress_channel, "Partnumber não encontrado na base de dados de simulação")

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
    partnumbers = [i for i in data.partnumbers.keys()]
    for i in range(total):
        p = partnumbers[i]
        try:
            redis_publisher.send_progress_update(
                data.progress_channel,
                ProgressSchema(current=i, total=total, message=f"[{i}] Processando partnumber {p} com Nexa IA")
            )
            result = pre_proc.get(p, None)
            time.sleep(2)
            if result is not None:
                redis_publisher.send_partial_result(
                    channel = data.progress_channel,
                    job_id = job_id,
                    result = result,
                    current = i,
                    total = total,
                    message = f"Classificação encontrada para o partnumber {p}"
                )
            time.sleep(3)
        except Exception as e:
            print(f"Erro ao processar classificação do partnumber {p}")
            pass
    redis_publisher.send_done_job(channel=data.progress_channel, job_id=job_id)
    return
