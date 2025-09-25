import os
from dotenv import load_dotenv

load_dotenv()


LITELLM_REQUEST_TIMEOUT = os.getenv("LITELLM_REQUEST_TIMEOUT") or 1800
