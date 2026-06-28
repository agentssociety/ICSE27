from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse
from src.infra.runway.runway_repo_impl import SQLAlchemyRunwayRepository


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=SQLAlchemyRunwayRepository)
    return repo


@pytest.fixture
def client(mock_repo):
    from src.api.runway.runway_router import router
    from src.config.database import get_db

    app = FastAPI()
    app.include_router(router, prefix="/runways")

    def override_get_db():
        return MagicMock()

    app.dependency_overrides[get_db] = override_get_db

    from src.api.runway.runway_router import _repo

    def override_repo():
        return mock_repo

    app.dependency_overrides[_repo] = override_repo
    return TestClient(app)


class TestRunwayAPI:
    """Tests for the Runway FastAPI router."""

    def test_create_runway(self, client, mock_repo):
        mock_repo.create.return_value = RunwayResponse(id="1", flight_id=None)
        response = client.post("/runways", json={})
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "1"

    def test_list_runways(self, client, mock_repo):
        mock_repo.get_all.return_value = [
            RunwayResponse(id="1", flight_id=None),
        ]
        response = client.get("/runways")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_get_runway_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = RunwayResponse(id="1", flight_id=None)
        response = client.get("/runways/1")
        assert response.status_code == 200
        assert response.json()["id"] == "1"

    def test_get_runway_not_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = None
        response = client.get("/runways/999")
        assert response.status_code == 404

    def test_update_runway(self, client, mock_repo):
        mock_repo.update.return_value = RunwayResponse(id="1", flight_id=2)
        response = client.put("/runways/1", json={"flight_id": 2})
        assert response.status_code == 200
        assert response.json()["flight_id"] == 2

    def test_delete_runway(self, client, mock_repo):
        mock_repo.delete.return_value = True
        response = client.delete("/runways/1")
        assert response.status_code == 204

    def test_delete_runway_not_found(self, client, mock_repo):
        mock_repo.delete.return_value = False
        response = client.delete("/runways/999")
        assert response.status_code == 404
