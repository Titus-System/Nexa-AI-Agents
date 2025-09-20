from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = 'Nexa-AI-Agents'
    ENVIRONMENT: str = 'development'

    @property
    def IS_PRODUCTION(self) -> bool:
        return self.ENVIRONMENT == 'production'

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0 

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = ConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )

    NEXA_API: str = "http://localhost:5000"


settings = Settings()