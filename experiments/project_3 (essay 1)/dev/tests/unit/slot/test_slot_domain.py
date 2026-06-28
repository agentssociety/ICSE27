from __future__ import annotations

import pytest

from src.domain.slot.Slot import (
    Slot,
    Resource,
    Actor,
    Permission,
    find_earliest_available_slot,
    SLOT_DURATION_MINUTES,
    GAP_MINUTES,
)


class TestSlotDomain:
    def test_slot_creation(self) -> None:
        """Test that a slot can be created with a time and resource."""
        actor = Actor(mayPerform=[Permission.READ])
        resource = Resource(owner=actor, accessible=[actor])
        slot = Slot()
        slot.create(time=100, resource=resource)
        assert slot.time == 100
        assert slot.resource == resource
        assert slot.isAvailable is True

    def test_slot_default_values(self) -> None:
        """Test that a slot has sensible default values."""
        slot = Slot()
        assert slot.isAvailable is True
        assert slot.time == 0
        assert slot.resource is None


class TestFindEarliestAvailableSlot:
    def test_no_existing_slots(self) -> None:
        """Test that with no existing slots, the reference time is returned."""
        result = find_earliest_available_slot(existing_slots=[], reference_time=0)
        assert result == 0

    def test_slot_before_first_existing(self) -> None:
        """Test that a slot can be placed before the first existing slot."""
        existing = [Slot(time=20)]
        result = find_earliest_available_slot(existing_slots=existing, reference_time=0)
        # 0 + 5 + 3 = 8 <= 20, so reference_time (0) works
        assert result == 0

    def test_slot_between_existing_slots(self) -> None:
        """Test that a slot can be placed between two existing slots."""
        existing = [Slot(time=0), Slot(time=30)]
        result = find_earliest_available_slot(existing_slots=existing, reference_time=0)
        # Slot 0: 0..5, gap 5..8. Slot 1 starts at 30.
        # 8 + 5 + 3 = 16 <= 30, so 8 is valid
        assert result == 8

    def test_slot_after_last_existing(self) -> None:
        """Test that a slot is placed after the last existing slot when no gap exists."""
        existing = [Slot(time=0), Slot(time=8)]
        result = find_earliest_available_slot(existing_slots=existing, reference_time=0)
        # Slot 0: 0..5, gap 5..8. Slot 1 starts at 8.
        # After slot 1: 8 + 5 + 3 = 16
        assert result == 16

    def test_slot_with_custom_reference_time(self) -> None:
        """Test that a slot respects a custom reference time."""
        existing = [Slot(time=10)]
        result = find_earliest_available_slot(existing_slots=existing, reference_time=15)
        # 15 + 5 + 3 = 23 > 10, so we need to place after the existing slot
        # After slot: 10 + 5 + 3 = 18
        assert result == 18

    def test_slot_respects_gap_and_duration_constants(self) -> None:
        """Test that the constants are set correctly."""
        assert SLOT_DURATION_MINUTES == 5
        assert GAP_MINUTES == 3
