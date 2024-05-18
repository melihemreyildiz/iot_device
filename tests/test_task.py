import pytest
import logging
from app.tasks import process_location
from app.database import SessionLocal, engine
from app.models import Base, Location, Device

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    logging.debug("Setting up the database")
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    logging.debug("Tearing down the database")


def test_process_location():
    logging.debug("Running test_process_location")

    db = SessionLocal()
    try:
        device = Device(name="Test Device")
        db.add(device)
        db.commit()
        db.refresh(device)

        data = '{"latitude": 40.7128, "longitude": -74.0060, "timestamp": "2023-05-01T12:00:00", "device_id": ' + str(
            device.id) + '}'

        logging.debug(f"Sending data to process_location: {data}")
        result = process_location(data)
        logging.debug(f"Result from process_location: {result}")

        location = db.query(Location).filter(Location.device_id == device.id).first()
        logging.debug(f"Location retrieved from DB: {location}")

        assert location is not None
        assert location.latitude == 40.7128
        assert location.longitude == -74.0060
        assert location.timestamp == "2023-05-01T12:00:00"
    except Exception as e:
        logging.error(f"Error in test_process_location: {e}")
        raise
    finally:
        db.close()
        logging.debug("Completed test_process_location")
