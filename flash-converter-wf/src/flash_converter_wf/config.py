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

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    UPLOAD_DIR: Path = _PROJECT_DIR / "uploads"


settings = Settings()
