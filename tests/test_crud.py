import pytest
from app import crud, models
from app.database import SessionLocal


@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()


def test_create_device(db):
    print("Running test_create_device")
    device = models.Device(name="Test Device")
    db.add(device)
    db.commit()
    db.refresh(device)
    assert device.id is not None
    assert device.name == "Test Device"
    print("Completed test_create_device")


def test_get_device(db):
    print("Running test_get_device")
    device = crud.get_device(db, 1)
    assert device is not None
    assert device.name == "Test Device"
    print("Completed test_get_device")


def test_delete_device(db):
    print("Running test_delete_device")
    crud.delete_device(db, 1)
    device = crud.get_device(db, 1)
    assert device is None
    print("Completed test_delete_device")
