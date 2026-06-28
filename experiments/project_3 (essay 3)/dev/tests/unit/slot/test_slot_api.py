from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from datetime import datetime

from src.dto.slot.slot_dto import SlotCreateRequest, SlotUpdateRequest, SlotResponse
from src.infra.slot.slot_repo_impl import SQLAlchemySlotRepository


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=SQLAlchemySlotRepository)
    return repo


@pytest.fixture
def client(mock_repo):
    from src.api.slot.slot_router import router
    from src.config.database import get_db

    app = FastAPI()
    app.include_router(router, prefix="/slots")

    def override_get_db():
        return MagicMock()

    app.dependency_overrides[get_db] = override_get_db

    from src.api.slot.slot_router import _repo

    def override_repo():
        return mock_repo

    app.dependency_overrides[_repo] = override_repo
    return TestClient(app)


class TestSlotAPI:
    """Tests for the Slot FastAPI router."""

    def test_create_slot(self, client, mock_repo):
        mock_repo.create.return_value = SlotResponse(
            id=1,
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
            flight_type="arrival",
            duration="5 minutes",
            gapAfter="3 minutes",
        )
        response = client.post(
            "/slots",
            json={
                "startTime": "2025-06-15T10:00:00",
                "endTime": "2025-06-15T10:05:00",
                "duration": "5 minutes",
                "gapAfter": "3 minutes",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["duration"] == "5 minutes"

    def test_list_slots(self, client, mock_repo):
        mock_repo.get_all.return_value = [
            SlotResponse(id=1, startTime=datetime(2025, 6, 15, 10, 0, 0), endTime=datetime(2025, 6, 15, 10, 5, 0), flight_type="arrival", duration="5 minutes", gapAfter="3 minutes"),
        ]
        response = client.get("/slots")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_get_slot_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = SlotResponse(
            id=1, startTime=datetime(2025, 6, 15, 10, 0, 0), endTime=datetime(2025, 6, 15, 10, 5, 0), flight_type="arrival", duration="5 minutes", gapAfter="3 minutes",
        )
        response = client.get("/slots/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_slot_not_found(self, client, mock_repo):
        mock_repo.get_by_id.return_value = None
        response = client.get("/slots/999")
        assert response.status_code == 404

    def test_update_slot(self, client, mock_repo):
        mock_repo.update.return_value = SlotResponse(
            id=1, startTime=datetime(2025, 6, 15, 10, 0, 0), endTime=datetime(2025, 6, 15, 10, 5, 0), flight_type="arrival", duration="10 minutes", gapAfter="3 minutes",
        )
        response = client.put("/slots/1", json={"duration": "10 minutes"})
        assert response.status_code == 200
        assert response.json()["duration"] == "10 minutes"

    def test_delete_slot(self, client, mock_repo):
        mock_repo.delete.return_value = True
        response = client.delete("/slots/1")
        assert response.status_code == 204

    def test_delete_slot_not_found(self, client, mock_repo):
        mock_repo.delete.return_value = False
        response = client.delete("/slots/999")
        assert response.status_code == 404
