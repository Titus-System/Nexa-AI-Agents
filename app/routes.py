from threading import Thread
import uuid
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.jobs import start_batch_classification_job, start_single_classification_job
from schemas.api_schemas import BatchClassificationRequest, SingleClassificationRequest

app_bp = Blueprint("process", __name__)


@app_bp.route("/single_partnumber", methods=["POST"])
def process_single_partnumber():
    try:
        data = SingleClassificationRequest.model_validate(request.get_json())
    except ValidationError as e:
        print(e)
        return jsonify({"error": "payload inválido"}), 400

    print("requisição recebida com sucesso")
    job_id = f"job-{uuid.uuid4()}"

    job_thread = Thread(target=start_single_classification_job, args=(data, job_id))
    job_thread.start()

    print(f"job {job_id} aceito para o partnumber '{data.partnumber}")
    return jsonify({"job_id": job_id}), 202


@app_bp.route("/batch_partnumbers", methods=["POST"])
def process_batch():
    try:
        data = BatchClassificationRequest.model_validate(request.get_json())
    except ValidationError as e:
        print(e)
        return jsonify({"error": "payload inválido"})
    
    job_id = f"job-{uuid.uuid4()}"

    job_thread = Thread(target=start_batch_classification_job, args=(data, job_id))
    job_thread.start()

    print(f"job {job_id} aceito para os partnumbers '{data.partnumbers}")
    return jsonify({"job_id": job_id}), 202