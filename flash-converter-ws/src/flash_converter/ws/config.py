"""
Web service configuration
"""

from flash_converter_wf.config import Settings as CommonSettings


class Settings(CommonSettings):
    """
    Web service configuration
    """

    # The FastAPI application uses the Celery application,
    # so the FastAPI settings should inherit the Celery settings
    # and extend them with the FastAPI-specific settings.

    # Configuration of the CORS middleware
    allow_origins: str = "http://localhost:5173,http://127.0.0.1:5173"


settings = Settings()
