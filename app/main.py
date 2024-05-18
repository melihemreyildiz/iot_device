from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/devices/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db=db, device=device)


@app.get("/devices/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@app.get("/devices/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device


@app.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    crud.delete_device(db, device_id=device_id)
    return {"detail": "Device deleted"}


@app.post("/devices/{device_id}/locations/", response_model=schemas.Location)
def create_location_for_device(device_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    crud.create_location_via_celery(location=location, device_id=device_id)
    # Return a dummy response as the actual creation is async
    return schemas.Location(id=0, device_id=device_id, **location.dict())


@app.get("/devices/{device_id}/locations/", response_model=List[schemas.Location])
def read_locations(device_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = crud.get_locations_by_device(db, device_id=device_id, skip=skip, limit=limit)
    return locations


@app.get("/devices/{device_id}/locations/last", response_model=schemas.Location)
def read_last_location(device_id: int, db: Session = Depends(get_db)):
    location = crud.get_last_location(db, device_id=device_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location
