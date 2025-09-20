import redis
from .config import settings


redis_client = redis.from_url(settings.REDIS_URL)