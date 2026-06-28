from __future__ import annotations

import pytest

from src.domain.urgency_level import UrgencyLevel, urgency_to_int, PriorityStatus, Permission


class TestUrgencyLevel:
    def test_urgency_level_enum_values(self) -> None:
        """UrgencyLevel has CRITICAL, HIGH, MEDIUM, LOW."""
        assert UrgencyLevel.CRITICAL.value == "critical"
        assert UrgencyLevel.HIGH.value == "high"
        assert UrgencyLevel.MEDIUM.value == "medium"
        assert UrgencyLevel.LOW.value == "low"

    def test_urgency_sort_order_critical_is_0(self) -> None:
        """CRITICAL has sort_order 0 (most urgent)."""
        assert UrgencyLevel.CRITICAL.sort_order() == 0

    def test_urgency_sort_order_high_is_1(self) -> None:
        """HIGH has sort_order 1."""
        assert UrgencyLevel.HIGH.sort_order() == 1

    def test_urgency_sort_order_medium_is_2(self) -> None:
        """MEDIUM has sort_order 2."""
        assert UrgencyLevel.MEDIUM.sort_order() == 2

    def test_urgency_sort_order_low_is_3(self) -> None:
        """LOW has sort_order 3 (least urgent)."""
        assert UrgencyLevel.LOW.sort_order() == 3

    def test_urgency_to_int_critical(self) -> None:
        """urgency_to_int returns 0 for critical."""
        assert urgency_to_int("critical") == 0

    def test_urgency_to_int_high(self) -> None:
        """urgency_to_int returns 1 for high."""
        assert urgency_to_int("high") == 1

    def test_urgency_to_int_medium(self) -> None:
        """urgency_to_int returns 2 for medium."""
        assert urgency_to_int("medium") == 2

    def test_urgency_to_int_low(self) -> None:
        """urgency_to_int returns 3 for low."""
        assert urgency_to_int("low") == 3

    def test_urgency_to_int_unknown_returns_99(self) -> None:
        """urgency_to_int returns 99 for unknown levels."""
        assert urgency_to_int("unknown") == 99

    def test_priority_status_enum(self) -> None:
        """PriorityStatus has expected values."""
        assert PriorityStatus.HIGHEST.value == "highest"
        assert PriorityStatus.HIGH.value == "high"
        assert PriorityStatus.MEDIUM.value == "medium"
        assert PriorityStatus.LOW.value == "low"
        assert PriorityStatus.LOWEST.value == "lowest"

    def test_permission_enum(self) -> None:
        """Permission has READ and WRITE."""
        assert Permission.READ.value == "read"
        assert Permission.WRITE.value == "write"
