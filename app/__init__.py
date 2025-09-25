from flask import Flask
from .config import settings
from .routes import app_bp


def create_app():
    app = Flask(__name__)
    app.config.update(**settings.model_dump())

    app.register_blueprint(app_bp, url_prefix="/process")

    return app