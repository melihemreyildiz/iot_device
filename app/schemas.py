from pydantic import BaseModel
from typing import List


class LocationBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: str


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    device_id: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int
    locations: List[Location] = []

    class Config:
        orm_mode = True
