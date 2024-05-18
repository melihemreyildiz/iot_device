from celery import Celery
from app import crud
from .database import SessionLocal
from .config import settings
import json
import logging

celery = Celery(__name__, broker=settings.rabbitmq_url)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task(name='app.tasks.process_location')
def process_location(data):
    db = SessionLocal()
    try:
        data_dict = json.loads(data)
        crud.create_location(db, location=data_dict, device_id=data_dict['device_id'])
        logger.info(f"Processed location: {data_dict}")
    except Exception as e:
        logger.error(f"Error processing location: {e}")
    finally:
        db.close()

