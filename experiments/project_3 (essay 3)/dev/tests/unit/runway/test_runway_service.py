from __future__ import annotations

import pytest
from typing import Optional
from src.dto.runway.runway_dto import RunwayCreate, RunwayUpdate, RunwayResponse
from src.repository.runway.runway_repository import RunwayRepository
from src.service.runway.runway_service import RunwayService


class FakeRunwayRepository:
    """In-memory repository for runway testing."""
    
    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def get_by_id(self, item_id: int) -> Optional[RunwayResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        return RunwayResponse(**row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RunwayResponse]:
        items = list(self._store.values())
        return [RunwayResponse(**r) for r in items[skip:skip + limit]]

    def create(self, data: RunwayCreate) -> RunwayResponse:
        row_id = self._next_id
        self._next_id += 1
        row = {
            "id": str(row_id),
            "flight_id": data.flight_id,
        }
        self._store[row_id] = row
        return RunwayResponse(**row)

    def update(self, item_id: int, data: RunwayUpdate) -> Optional[RunwayResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                row[key] = value
        self._store[item_id] = row
        return RunwayResponse(**row)

    def delete(self, item_id: int) -> bool:
        if item_id in self._store:
            del self._store[item_id]
            return True
        return False


class TestRunwayService:
    """Tests for RunwayService."""

    def setup_method(self) -> None:
        self.repo = FakeRunwayRepository()
        self.service = RunwayService(repository=self.repo)

    def test_create_runway(self) -> None:
        data = RunwayCreate()
        result = self.service.create_runway(data)
        assert result is not None
        assert result.id is not None

    def test_get_runway_found(self) -> None:
        created = self.service.create_runway(RunwayCreate())
        result = self.service.get_by_id(int(created.id))
        assert result is not None

    def test_get_runway_not_found(self) -> None:
        result = self.service.get_by_id(999)
        assert result is None

    def test_get_all_runways(self) -> None:
        self.service.create_runway(RunwayCreate())
        self.service.create_runway(RunwayCreate())
        results = self.service.get_all()
        assert len(results) == 2

    def test_close_runway_and_reassign_no_alternatives(self) -> None:
        created = self.service.create_runway(RunwayCreate())
        with pytest.raises(ValueError, match="No alternative runways available"):
            self.service.close_runway_and_reassign(int(created.id), [])

    def test_close_runway_and_reassign_with_alternatives(self) -> None:
        r1 = self.service.create_runway(RunwayCreate())
        r2 = self.service.create_runway(RunwayCreate())
        result = self.service.close_runway_and_reassign(int(r1.id), [int(r2.id)])
        assert result["closed_runway_id"] == int(r1.id)
        assert len(result["reassigned_to"]) > 0

    def test_close_runway_not_found(self) -> None:
        with pytest.raises(ValueError, match="Runway with id 999 not found"):
            self.service.close_runway_and_reassign(999, [1, 2])

    def test_delete_runway(self) -> None:
        created = self.service.create_runway(RunwayCreate())
        assert self.service.delete_runway(int(created.id)) is True
        assert self.service.get_by_id(int(created.id)) is None

    def test_constructor_none_repo(self) -> None:
        with pytest.raises(ValueError, match="repository must not be None"):
            RunwayService(repository=None)
