from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(String)

    device = relationship("Device", back_populates="locations")


Device.locations = relationship("Location", order_by=Location.id, back_populates="device")
