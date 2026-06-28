from __future__ import annotations

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.config.database import get_db, engine, Base

# Import ORM models so they register with Base.metadata
import src.orm.patient.patient_orm  # noqa: F401


@pytest.fixture(autouse=True, scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app():
    app = FastAPI()

    from src.api.patient.patient_router import router
    app.include_router(router, prefix="/patients")
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


class TestPatientAPI:
    def test_list_patients_empty(self, client):
        response = client.get("/patients")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_patient(self, client):
        now = datetime.now(timezone.utc)
        payload = {
            "symptoms": "fever",
            "urgencyLevel": 5,
            "queuePosition": 0,
            "arrivalTime": now.isoformat(),
            "urgency": "5",
        }
        response = client.post("/patients", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["symptoms"] == "fever"
        assert "id" in data
        assert data["urgencyLevel"] == 5

    def test_create_and_retrieve(self, client):
        now = datetime.now(timezone.utc)
        payload = {
            "symptoms": "cough",
            "urgencyLevel": 3,
            "queuePosition": 1,
            "arrivalTime": now.isoformat(),
            "urgency": "3",
        }
        create_resp = client.post("/patients", json=payload)
        assert create_resp.status_code == 201
        patient_id = create_resp.json()["id"]

        get_resp = client.get(f"/patients/{patient_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["symptoms"] == "cough"

    def test_dashboard_returns_list(self, client):
        response = client.get("/patients/dashboard")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_dashboard_shows_patients(self, client):
        now = datetime.now(timezone.utc)
        payload = {
            "symptoms": "chest pain",
            "urgencyLevel": 1,
            "queuePosition": 0,
            "arrivalTime": now.isoformat(),
            "urgency": "1",
        }
        create_resp = client.post("/patients", json=payload)
        patient_id = create_resp.json()["id"]

        response = client.get("/patients/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        dashboard_item = data[0]
        assert dashboard_item["patient_id"] == patient_id
        assert dashboard_item["urgency_level"] == 1
        assert dashboard_item["estimated_wait_minutes"] >= 10
