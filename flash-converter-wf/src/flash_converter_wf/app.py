from celery import Celery

from flash_converter_wf.config import settings

celery_app = Celery(
    "flash_converter_wf.app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.broker_connection_retry_on_startup = settings.BROKER_CONNECTION_RETRY_ON_STARTUP
