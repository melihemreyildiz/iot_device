from sqlalchemy.orm import Session
from . import models, schemas
from app import tasks
import json


def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(name=device.name)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_devices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Device).offset(skip).limit(limit).all()


def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()


def delete_device(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        return None
    db.delete(db_device)
    db.commit()
    return db_device


def create_location(db: Session, location: dict, device_id: int):
    location_data = {k: v for k, v in location.items() if k != 'device_id'}
    db_location = models.Location(**location_data, device_id=device_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def create_location_via_celery(location: schemas.LocationCreate, device_id: int):
    data = location.dict()
    data['device_id'] = device_id
    tasks.process_location.delay(json.dumps(data))


def get_locations_by_device(db: Session, device_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Location).filter(models.Location.device_id == device_id).offset(skip).limit(limit).all()


def get_last_location(db: Session, device_id: int):
    return db.query(models.Location).filter(models.Location.device_id == device_id).order_by(
        models.Location.timestamp.desc()).first()
