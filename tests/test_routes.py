import pytest
from unittest.mock import patch, MagicMock
from app.routes import app_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(app_bp, url_prefix="/process")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_process_single_partnumber_success(client):
    payload = {
        "progress_channel": "test_channel",
        "partnumber": "12345-XYZ",
        "description": "desc",
        "manufacturer": "manu",
        "supplier": "sup"
    }
    with patch("app.routes.start_single_classification_job") as mock_job:
        response = client.post("/process/single_partnumber", json=payload)
        assert response.status_code == 202
        data = response.get_json()
        assert "job_id" in data
        assert data["job_id"].startswith("job-")
        mock_job.assert_called_once()

def test_process_single_partnumber_invalid_payload(client):
    # Missing required fields
    payload = {"description": "desc"}
    response = client.post("/process/single_partnumber", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "payload inválido"
