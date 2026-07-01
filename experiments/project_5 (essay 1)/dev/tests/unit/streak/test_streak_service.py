from __future__ import annotations

import pytest
from src.service.streak.streak_service import StreakService


class TestStreakService:
    def test_record_activity(self) -> None:
        svc = StreakService()
        result = svc.record_activity("student_1", "2024-01-01")
        assert result == 1

    def test_get_current_streak_default(self) -> None:
        svc = StreakService()
        assert svc.get_current_streak("student_1") == 0

    def test_get_longest_streak_default(self) -> None:
        svc = StreakService()
        assert svc.get_longest_streak("student_1") == 0

    def test_reset_streak(self) -> None:
        svc = StreakService()
        svc.reset_streak("student_1")  # Should not raise
