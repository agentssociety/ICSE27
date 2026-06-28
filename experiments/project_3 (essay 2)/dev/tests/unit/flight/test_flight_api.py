from __future__ import annotations

from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from src.config.database import Base, get_db
from src.api.flight.flight_router import router
from src.orm.flight.flight_orm import FlightORM


@pytest.fixture(scope="module")
def client():
    """Create a clean FastAPI app with in-memory SQLite for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    test_app = FastAPI()
    test_app.include_router(router, prefix="/flights", tags=["Flight"])

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db
    return TestClient(test_app)


class TestFlightAPI:
    def test_create_flight_endpoint(self, client: TestClient) -> None:
        """Test POST /flights creates a new flight."""
        response = client.post(
            "/flights",
            json={
                "flightNumber": "AA100",
                "airline": "American Airlines",
                "origin": "JFK",
                "destination": "LHR",
                "scheduledTime": "2025-07-01T08:00:00",
                "type": "departure",
            },
        )
        assert response.status_code == 201, f"Got {response.status_code}: {response.text}"
        data = response.json()
        assert data["flightNumber"] == "AA100"

    def test_list_flights(self, client: TestClient) -> None:
        """Test GET /flights returns a list."""
        response = client.get("/flights")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_flight_not_found(self, client: TestClient) -> None:
        """Test GET /flights/{id} returns 404 for non-existent flight."""
        response = client.get("/flights/99999")
        assert response.status_code == 404

    def test_delete_flight_not_found(self, client: TestClient) -> None:
        """Test DELETE /flights/{id} returns 404 for non-existent flight."""
        response = client.delete("/flights/99999")
        assert response.status_code == 404

    def test_create_then_list(self, client: TestClient) -> None:
        """Test that creating a flight then listing returns it."""
        client.post(
            "/flights",
            json={
                "flightNumber": "BB200",
                "airline": "British Airways",
                "origin": "LHR",
                "destination": "JFK",
                "scheduledTime": "2025-07-01T10:00:00",
                "type": "departure",
            },
        )
        response = client.get("/flights")
        assert response.status_code == 200
        data = response.json()
        numbers = [f["flightNumber"] for f in data]
        assert "BB200" in numbers

    def test_create_then_get(self, client: TestClient) -> None:
        """Test that creating a flight then fetching it by ID works."""
        create_resp = client.post(
            "/flights",
            json={
                "flightNumber": "CC300",
                "airline": "Delta",
                "origin": "JFK",
                "destination": "MIA",
                "scheduledTime": "2025-07-01T12:00:00",
                "type": "departure",
            },
        )
        flight_id = create_resp.json()["id"]

        get_resp = client.get(f"/flights/{flight_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["flightNumber"] == "CC300"

    def test_create_then_delete(self, client: TestClient) -> None:
        """Test that creating a flight then deleting it works."""
        create_resp = client.post(
            "/flights",
            json={
                "flightNumber": "DD400",
                "airline": "United",
                "origin": "ORD",
                "destination": "LAX",
                "scheduledTime": "2025-07-01T14:00:00",
                "type": "departure",
            },
        )
        flight_id = create_resp.json()["id"]

        delete_resp = client.delete(f"/flights/{flight_id}")
        assert delete_resp.status_code == 204

        get_resp = client.get(f"/flights/{flight_id}")
        assert get_resp.status_code == 404

    def test_create_flight_invalid_data(self, client: TestClient) -> None:
        """Test that missing required fields return 422."""
        response = client.post("/flights", json={})
        assert response.status_code == 422
