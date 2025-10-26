import os
from dotenv import load_dotenv

load_dotenv()


LITELLM_REQUEST_TIMEOUT = os.getenv("LITELLM_REQUEST_TIMEOUT") or 1800
OLLAMA_URI = os.getenv("OLLAMA_URI") or "http://127.0.0.1:11434"
