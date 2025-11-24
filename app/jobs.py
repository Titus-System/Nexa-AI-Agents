from app.simul import run_batch_simul, run_single_simul
from schemas.api_schemas import (
    BatchClassificationRequest,
    ProgressSchema,
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
        progress_schema = ProgressSchema(
            current=1, total=5, message="Analisando dados no servidor Nexa-IA"
        )
        redis_publisher.send_progress_update(data.progress_channel, progress_schema)
        manager_agent(channel=data.progress_channel, job_id=job_id, data=data)

        return

    except Exception as e:
        redis_publisher.send_failed_processing(data.progress_channel, str(e))



def run_demo(data: SingleClassificationRequest, job_id: str):
    run_single_simul(data, job_id)


def start_batch_classification_job(data: BatchClassificationRequest, job_id: str):
    # run_batch_simul(data, job_id)
    print(f"Iniciando job para classificação dos partnumbers: {data.partnumbers} no canal {data.progress_channel}")
    total = len(data.partnumbers)
    if total == 0:
        redis_publisher.send_failed_processing(
            data.progress_channel, 
            "Nenhum partnumber encontrado para iniciar job de classificação.",
            job_id
        )
        return
    current = 1
    redis_publisher.send_progress_update(
        data.progress_channel,
        ProgressSchema(current=current, total=total, message=f"Iniciando Classificação con Nexa IA. Aguarde pelos resultados.")
    )
    for pn, info in data.partnumbers.items():
        try:
            redis_publisher.send_progress_update(
                data.progress_channel,
                ProgressSchema(current=current, total=total, message=f"[{current}] Processando partnumber {pn} com Nexa IA")
            )
            result = manager_agent(data.progress_channel, job_id, info)
            if result:
                redis_publisher.send_partial_result(
                    channel = data.progress_channel,
                    job_id = job_id,
                    result = result,
                    current = current,
                    total = total,
                    message = f"Classificação encontrada para o partnumber {pn}"
                )
        except Exception as e:
            print(f"Erro ao processar classificação do partnumber {pn}: {e}")
            redis_publisher.send_failed_processing(data.progress_channel, f"Erro ao processar partnumber{pn}", job_id)
            pass
    redis_publisher.send_done_job(channel=data.progress_channel, job_id=job_id)
    return