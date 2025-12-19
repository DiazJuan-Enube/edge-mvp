import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

# Ruta al archivo .env (en el directorio app/)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "polymarket-read-api"
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str  # async SQLAlchemy URL

    ENABLE_REDIS: bool = False
    REDIS_URL: str | None = None

settings = Settings()
