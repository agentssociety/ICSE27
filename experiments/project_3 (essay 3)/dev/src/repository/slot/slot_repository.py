from __future__ import annotations

from typing import Optional, Protocol
from datetime import datetime

from src.dto.slot.slot_dto import SlotCreateRequest, SlotUpdateRequest, SlotResponse


class SlotRepository(Protocol):
    """Interface for slot data access."""

    def get_by_id(self, item_id: int) -> Optional[SlotResponse]: ...

    def get_all(self, skip: int = 0, limit: int = 100) -> list[SlotResponse]: ...

    def create(self, data: SlotCreateRequest) -> SlotResponse: ...

    def update(self, item_id: int, data: SlotUpdateRequest) -> Optional[SlotResponse]: ...

    def delete(self, item_id: int) -> bool: ...

    def get_slots_by_time_range(self, startTime: datetime, endTime: datetime) -> list[SlotResponse]: ...

    def get_all_slots(self) -> list[SlotResponse]: ...
