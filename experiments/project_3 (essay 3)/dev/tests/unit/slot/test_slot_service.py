from __future__ import annotations

import pytest
from typing import Optional
from datetime import datetime, timedelta

from src.dto.slot.slot_dto import SlotCreateRequest, SlotUpdateRequest, SlotResponse
from src.repository.slot.slot_repository import SlotRepository
from src.service.slot.slot_service import SlotServiceImpl, SlotService


class FakeSlotRepository:
    """In-memory repository for testing."""
    
    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def get_by_id(self, item_id: int) -> Optional[SlotResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        return SlotResponse(**row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SlotResponse]:
        items = list(self._store.values())
        return [SlotResponse(**r) for r in items[skip:skip + limit]]

    def create(self, data: SlotCreateRequest) -> SlotResponse:
        row_id = self._next_id
        self._next_id += 1
        row = {
            "id": row_id,
            "startTime": data.startTime.isoformat() if hasattr(data.startTime, 'isoformat') else str(data.startTime),
            "endTime": data.endTime.isoformat() if hasattr(data.endTime, 'isoformat') else str(data.endTime),
            "flight_type": data.flight_type,
            "duration": data.duration,
            "gapAfter": data.gapAfter,
        }
        self._store[row_id] = row
        return SlotResponse(**row)

    def update(self, item_id: int, data: SlotUpdateRequest) -> Optional[SlotResponse]:
        row = self._store.get(item_id)
        if row is None:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                row[key] = value
        self._store[item_id] = row
        return SlotResponse(**row)

    def delete(self, item_id: int) -> bool:
        if item_id in self._store:
            del self._store[item_id]
            return True
        return False

    def get_slots_by_time_range(self, startTime: datetime, endTime: datetime) -> list[SlotResponse]:
        result = []
        for row in self._store.values():
            st = datetime.fromisoformat(row["startTime"]) if isinstance(row["startTime"], str) else row["startTime"]
            et = datetime.fromisoformat(row["endTime"]) if isinstance(row["endTime"], str) else row["endTime"]
            if st >= startTime and et <= endTime:
                result.append(SlotResponse(**row))
        return result

    def get_all_slots(self) -> list[SlotResponse]:
        return [SlotResponse(**r) for r in self._store.values()]


class TestSlotServiceImpl:
    """Tests for SlotServiceImpl."""

    def setup_method(self) -> None:
        self.repo = FakeSlotRepository()
        self.service: SlotService = SlotServiceImpl(repository=self.repo)

    def test_allocate_slot_success(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        result = self.service.allocate_slot(data)
        assert result.id == 1
        assert result.duration == "5 minutes"

    def test_allocate_slot_end_before_start(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 5, 0),
            endTime=datetime(2025, 6, 15, 10, 0, 0),
        )
        with pytest.raises(ValueError, match="endTime must be after startTime"):
            self.service.allocate_slot(data)

    def test_allocate_slot_invalid_duration(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 10, 0),  # 10 minutes
        )
        with pytest.raises(ValueError, match="Slot duration must be exactly 5 minutes"):
            self.service.allocate_slot(data)

    def test_allocate_slot_gap_violation(self) -> None:
        # Create first slot
        data1 = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        self.service.allocate_slot(data1)
        # Second slot too close (1 min gap instead of 3)
        data2 = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 6, 0),
            endTime=datetime(2025, 6, 15, 10, 11, 0),
        )
        with pytest.raises(ValueError, match="Adjacent gap of at least 3 minutes"):
            self.service.allocate_slot(data2)

    def test_get_slot_found(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        created = self.service.allocate_slot(data)
        result = self.service.get_slot(created.id)
        assert result is not None
        assert result.id == created.id

    def test_get_slot_not_found(self) -> None:
        result = self.service.get_slot(999)
        assert result is None

    def test_get_slot_negative_id(self) -> None:
        with pytest.raises(ValueError, match="slot_id must be non-negative"):
            self.service.get_slot(-1)

    def test_get_all_slots(self) -> None:
        data1 = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        data2 = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 8, 0),
            endTime=datetime(2025, 6, 15, 10, 13, 0),
        )
        self.service.allocate_slot(data1)
        self.service.allocate_slot(data2)
        results = self.service.get_all_slots()
        assert len(results) == 2

    def test_update_slot(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        created = self.service.allocate_slot(data)
        update_data = SlotUpdateRequest(duration="10 minutes")
        result = self.service.update_slot(created.id, update_data)
        assert result is not None

    def test_delete_slot(self) -> None:
        data = SlotCreateRequest(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        created = self.service.allocate_slot(data)
        assert self.service.delete_slot(created.id) is True
        assert self.service.get_slot(created.id) is None

    def test_constructor_none_repo(self) -> None:
        with pytest.raises(ValueError, match="repository must not be None"):
            SlotServiceImpl(repository=None)
