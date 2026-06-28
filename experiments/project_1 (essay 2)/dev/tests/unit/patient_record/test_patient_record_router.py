from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.config.database import get_db, engine, Base

# Import ORM models so they register with Base.metadata
import src.orm.patient_record.patient_record_orm  # noqa: F401


@pytest.fixture(autouse=True, scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app():
    app = FastAPI()

    from src.api.patient_record.patient_record_router import router
    app.include_router(router, prefix="/patient_records")
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestPatientRecordRouter:
    def test_list_empty(self, client):
        response = client.get("/patient_records")
        assert response.status_code == 200
        assert response.json() == []

    def test_create(self, client):
        payload = {"owner_id": 1}
        response = client.post("/patient_records", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["owner_id"] == 1
        assert "id" in data

    def test_create_and_retrieve(self, client):
        payload = {"owner_id": 42}
        create_resp = client.post("/patient_records", json=payload)
        assert create_resp.status_code == 201
        record_id = create_resp.json()["id"]

        get_resp = client.get(f"/patient_records/{record_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["owner_id"] == 42

    def test_get_not_found(self, client):
        response = client.get("/patient_records/999")
        assert response.status_code == 404

    def test_update(self, client):
        create_resp = client.post("/patient_records", json={"owner_id": 1})
        record_id = create_resp.json()["id"]

        update_resp = client.put(f"/patient_records/{record_id}", json={"owner_id": 2})
        assert update_resp.status_code == 200
        assert update_resp.json()["owner_id"] == 2

    def test_update_not_found(self, client):
        response = client.put("/patient_records/999", json={"owner_id": 1})
        assert response.status_code == 404

    def test_delete(self, client):
        create_resp = client.post("/patient_records", json={"owner_id": 1})
        record_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/patient_records/{record_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/patient_records/{record_id}")
        assert get_resp.status_code == 404

    def test_delete_not_found(self, client):
        response = client.delete("/patient_records/999")
        assert response.status_code == 404

    def test_list_after_create(self, client):
        client.post("/patient_records", json={"owner_id": 10})
        client.post("/patient_records", json={"owner_id": 20})
        response = client.get("/patient_records")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
