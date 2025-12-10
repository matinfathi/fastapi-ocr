from celery import Celery

from .config import settings


celery_app = Celery(
    "ocr_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.api.ocr.services"]
)


celery_app.conf.task_routes = {
    "tasks.process_ocr_document": "main-queue"
}
