"""
Web service configuration
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_HERE = Path(__file__).parent
_PROJECT_DIR = next(iter(p for p in _HERE.parents if p.name == "flash-converter"), _HERE.parent)


class Settings(BaseSettings):
    """
    Task manager configuration
    """

    # read from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Celery broker URL (e.g. amqp://guest:guest@localhost:5672// for RabbitMQ).
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"

    # Celery result backend URL (e.g. redis://localhost:6379/0 for Redis).
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Specifies whether Celery should retry to establish a connection during startup.
    # When the Celery worker starts, it will try to establish a connection with the broker.
    # If the connection fails, the worker will continue to try to establish a connection with the broker.
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True

    # Directory to store uploaded files (a volume or mount point).
    UPLOAD_DIR: Path = _PROJECT_DIR / "uploads"


settings = Settings()
