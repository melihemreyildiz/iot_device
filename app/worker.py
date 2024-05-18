from .tasks import process_location

from celery import Celery
from .config import settings

celery = Celery(__name__, broker=settings.rabbitmq_url)
