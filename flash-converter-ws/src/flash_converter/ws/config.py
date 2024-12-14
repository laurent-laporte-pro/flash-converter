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


settings = Settings()
