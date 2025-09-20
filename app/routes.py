from threading import Thread
import time
import uuid
from flask import Blueprint, json, request, jsonify
from pydantic import ValidationError

from schemas.api_schemas import DoneProcessing, FailedProcessing, ProgressSchema, SingleClassification, SingleClassificationRequest, UpdateProgressStatus
from .extensions import redis_client

app_bp = Blueprint("process", __name__)


@app_bp.route("/single_partnumber", methods=["POST"])
def process_single_partnumber():
    try:
        data = SingleClassificationRequest.model_validate(request.get_json())
    except ValidationError as e:
        print(e)
        return jsonify({"error": "payload inválido"}), 400

    partnumber = data.partnumber
    progress_channel = data.progress_channel

    job_thread = Thread(target=mock_classification_job, args=(partnumber, progress_channel))
    job_thread.start()

    job_id = f"job-{uuid.uuid4()}"
    print(f"job {job_id} aceito para o partnumber '{partnumber}")
    return jsonify({"job_id": job_id}), 202


def mock_classification_job(partnumber:str, channel:str):
    print(f"Iniciando job para partnumber {partnumber} no canal {channel}")
    try:
        for i in range(3):
            time.sleep(1)
            update_processing = UpdateProgressStatus(
                status = 'processing',
                progress = ProgressSchema(
                    current = i + 1,
                    total = 3,
                    message = "Analisando dados no servidor Nexa-IA"
                )
            )
            redis_client.publish(channel, json.dumps(update_processing.model_dump()))

        time.sleep(1)
        done_processing = DoneProcessing(
            status='done',
            result = SingleClassification(
                ncm = "123456788",
                description = "Descrição detalhada do produto",
                exception = "01",
                nve = "01",
                fabricante = "fábrica Nexa",
                endereco = "av pequim",
                pais = "China",
                confidence_score = 0.98                
            )
        )
        redis_client.publish(channel, json.dumps(done_processing.model_dump()))
        return
    except Exception as e:
        failed_processing = FailedProcessing(
            status = 'failed',
            error = str(e)
        ) 
        redis_client.publish(channel, json.dumps(failed_processing.model_dump()))