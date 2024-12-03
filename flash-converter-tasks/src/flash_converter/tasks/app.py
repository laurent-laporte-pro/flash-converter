from celery import Celery

from flash_converter.tasks.config import settings

celery_app = Celery(
    "flash_converter.tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)
