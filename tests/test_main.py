import pytest
from httpx import AsyncClient
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base
import asyncio


print("1")

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_create_device():
    print("Running test_create_device")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await asyncio.wait_for(ac.post("/devices/", json={"name": "Test Device"}), timeout=2)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Device"
    print("Completed test_create_device")


@pytest.mark.asyncio
async def test_read_devices():
    print("Running test_read_devices")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await asyncio.wait_for(ac.get("/devices/"), timeout=2)
    assert response.status_code == 200
    assert len(response.json()) == 1
    print("Completed test_read_devices")


@pytest.mark.asyncio
async def test_read_device():
    print("Running test_read_device")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await asyncio.wait_for(ac.post("/devices/", json={"name": "Test Device"}), timeout=2)
        device_id = response.json()["id"]
        response = await asyncio.wait_for(ac.get(f"/devices/{device_id}"), timeout=2)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Device"
    print("Completed test_read_device")


@pytest.mark.asyncio
async def test_delete_device():
    print("Running test_delete_device")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await asyncio.wait_for(ac.post("/devices/", json={"name": "Device to Delete"}), timeout=2)
        device_id = response.json()["id"]
        response = await asyncio.wait_for(ac.delete(f"/devices/{device_id}"), timeout=2)
        assert response.status_code == 200
        response = await asyncio.wait_for(ac.get(f"/devices/{device_id}"), timeout=2)
        assert response.status_code == 404
    print("Completed test_delete_device")
