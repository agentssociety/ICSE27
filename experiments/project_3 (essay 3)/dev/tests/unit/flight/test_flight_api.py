from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.dto.flight.flight_dto import FlightCreate, FlightUpdate, FlightResponse
from src.infra.flight.flight_repo_impl import SQLAlchemyFlightRepository


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=SQLAlchemyFlightRepository)
    return repo


@pytest.fixture
def client(mock_repo):
    from src.api.flight.flight_router import router
    from src.config.database import get_db

    app = FastAPI()
    app.include_router(router, prefix="/flights")

    # Override get_db to return a mock session
    def override_get_db():
        return MagicMock()

    app.dependency_overrides[get_db] = override_get_db

    # Also override _repo to return our mock directly
    from src.api.flight.flight_router import _repo

    def override_repo():
        return mock_repo

    app.dependency_overrides[_repo] = override_repo
    return TestClient(app)


class TestFlightAPI:
    """Tests for the Flight FastAPI router."""

    def test_create_flight(self, client, mock_repo):
        mock_repo.create.return_value = FlightResponse(
            id=1,
            flightNumber="BA123",
            origin="LHR",
            destination="JFK",
            estimatedDepartureTime="2025-06-15T10:00:00Z",
        )
        response = client.post(
            "/flights",
            json={
                "flightNumber": "BA123",
                "origin": "LHR",
                "destination": "JFK",
                "estimatedDepartureTime": "2025-06-15T10:00:00Z",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["flightNumber"] == "BA123"
        assert data["id"] == 1

    def test_list_flights(self, client, mock_repo):
        mock_repo.get_all.return_value = [
            FlightResponse(id=1, flightNumber="BA1", origin="A", destination="B", estimatedDepartureTime="T1"),
            FlightResponse(id=2, flightNumber="BA2", origin="C", destination="D", estimatedDepartureTime="T2"),
        ]
        response = client.get("/flights")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_flight_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = FlightResponse(
            id=1, flightNumber="BA123", origin="LHR", destination="JFK", estimatedDepartureTime="T1"
        )
        response = client.get("/flights/1")
        assert response.status_code == 200
        assert response.json()["flightNumber"] == "BA123"

    def test_get_flight_not_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = None
        response = client.get("/flights/999")
        assert response.status_code == 404

    def test_update_flight(self, client, mock_repo):
        mock_repo.update.return_value = FlightResponse(
            id=1, flightNumber="BA123", origin="LHR", destination="LAX", estimatedDepartureTime="T1"
        )
        response = client.put("/flights/1", json={"destination": "LAX"})
        assert response.status_code == 200
        assert response.json()["destination"] == "LAX"

    def test_update_flight_not_found(self, client, mock_repo):
        mock_repo.update.return_value = None
        response = client.put("/flights/999", json={"destination": "LAX"})
        assert response.status_code == 404

    def test_delete_flight(self, client, mock_repo):
        mock_repo.delete.return_value = True
        response = client.delete("/flights/1")
        assert response.status_code == 204

    def test_delete_flight_not_found(self, client, mock_repo):
        mock_repo.delete.return_value = False
        response = client.delete("/flights/999")
        assert response.status_code == 404
