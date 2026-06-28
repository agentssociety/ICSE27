from __future__ import annotations

import pytest
from datetime import datetime, timedelta

from src.domain.slot.Slot import Slot, SlotId, SlotCreatedEvent, SlotUpdatedEvent, Permission, State, Actor, Resource


class TestSlotDomain:
    """Tests for the Slot domain class."""

    def test_create_slot_defaults(self) -> None:
        start = datetime(2025, 6, 15, 10, 0, 0)
        end = datetime(2025, 6, 15, 10, 5, 0)
        slot = Slot(startTime=start, endTime=end)
        assert slot.startTime == start
        assert slot.endTime == end
        assert slot.duration == timedelta(minutes=5)
        assert slot.gapAfter == timedelta(minutes=3)

    def test_slot_duration_correct(self) -> None:
        start = datetime(2025, 6, 15, 10, 0, 0)
        end = datetime(2025, 6, 15, 10, 5, 0)
        slot = Slot(startTime=start, endTime=end)
        assert slot.endTime - slot.startTime == timedelta(minutes=5)

    def test_check_overlap_detects_overlap(self) -> None:
        slot1 = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        slot2 = Slot(
            startTime=datetime(2025, 6, 15, 10, 3, 0),
            endTime=datetime(2025, 6, 15, 10, 8, 0),
        )
        overlapping = slot1.checkOverlap(slot2, [slot1])
        assert overlapping is True

    def test_check_overlap_no_overlap(self) -> None:
        slot1 = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        slot2 = Slot(
            startTime=datetime(2025, 6, 15, 10, 8, 0),
            endTime=datetime(2025, 6, 15, 10, 13, 0),
        )
        overlapping = slot1.checkOverlap(slot2, [slot1])
        assert overlapping is False

    def test_check_adjacent_gap_enough_gap(self) -> None:
        slot1 = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        slot2 = Slot(
            startTime=datetime(2025, 6, 15, 10, 8, 0),
            endTime=datetime(2025, 6, 15, 10, 13, 0),
        )
        # 3-minute gap: slot1 ends at 10:05, slot2 starts at 10:08 — 3 min gap
        assert slot2.checkAdjacentGap(slot2, [slot1]) is True

    def test_check_adjacent_gap_not_enough_gap(self) -> None:
        slot1 = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        slot2 = Slot(
            startTime=datetime(2025, 6, 15, 10, 6, 0),
            endTime=datetime(2025, 6, 15, 10, 11, 0),
        )
        # Only 1-minute gap
        assert slot2.checkAdjacentGap(slot2, [slot1]) is False

    def test_verify_allocations_valid(self) -> None:
        slot1 = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        slot2 = Slot(
            startTime=datetime(2025, 6, 15, 10, 8, 0),
            endTime=datetime(2025, 6, 15, 10, 13, 0),
        )
        assert slot1.verifyAllocations([slot1, slot2]) is True

    def test_verify_allocations_invalid_duration(self) -> None:
        slot = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 10, 0),  # 10 minutes, not 5
        )
        assert slot.verifyAllocations([slot]) is False

    def test_verify_allocations_empty(self) -> None:
        slot = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        assert slot.verifyAllocations([]) is True

    def test_create_method_valid(self) -> None:
        slot = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        result = slot.create(
            startTime=datetime(2025, 6, 15, 11, 0, 0),
            endTime=datetime(2025, 6, 15, 11, 5, 0),
        )
        assert result.startTime == datetime(2025, 6, 15, 11, 0, 0)
        assert result.endTime == datetime(2025, 6, 15, 11, 5, 0)

    def test_create_method_invalid_duration(self) -> None:
        slot = Slot(
            startTime=datetime(2025, 6, 15, 10, 0, 0),
            endTime=datetime(2025, 6, 15, 10, 5, 0),
        )
        with pytest.raises(ValueError, match="Slot duration must be exactly 5 minutes"):
            slot.create(
                startTime=datetime(2025, 6, 15, 11, 0, 0),
                endTime=datetime(2025, 6, 15, 11, 10, 0),  # 10 minutes
            )

    def test_slot_id_creation(self) -> None:
        sid = SlotId()
        assert isinstance(sid, SlotId)

    def test_slot_created_event(self) -> None:
        event = SlotCreatedEvent()
        assert isinstance(event, SlotCreatedEvent)

    def test_slot_updated_event(self) -> None:
        event = SlotUpdatedEvent()
        assert isinstance(event, SlotUpdatedEvent)
