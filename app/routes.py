from threading import Thread
import time
import uuid
from flask import Blueprint, json, request, jsonify
from pydantic import ValidationError
from redis import Redis
import redis

from app.jobs import start_single_classification_job
from schemas.api_schemas import ProgressSchema, SingleClassification, SingleClassificationRequest
from .extensions import redis_publisher

app_bp = Blueprint("process", __name__)


@app_bp.route("/single_partnumber", methods=["POST"])
def process_single_partnumber():
    try:
        data = SingleClassificationRequest.model_validate(request.get_json())
    except ValidationError as e:
        print(e)
        return jsonify({"error": "payload inválido"}), 400

    job_id = f"job-{uuid.uuid4()}"

    job_thread = Thread(target=start_single_classification_job, args=(data, job_id))
    job_thread.start()

    print(f"job {job_id} aceito para o partnumber '{data.partnumber}")
    return jsonify({"job_id": job_id}), 202