from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("digital_twin", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_default_queue = "default"
celery_app.conf.broker_connection_retry_on_startup = True


@celery_app.task(name="ping")
def ping() -> str:
    """Smoke-test task proving the worker/broker wiring works end to end."""
    return "pong"
