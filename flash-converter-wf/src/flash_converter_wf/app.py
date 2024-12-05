from celery import Celery

from flash_converter_wf.config import settings

celery_app = Celery(
    "flash_converter_wf.app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
