from celery import Celery


celery_app = Celery(
    "ocr_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.api.ocr.services"]
)


celery_app.conf.task_routes = {
    "tasks.process_ocr_document": "main-queue"
}
