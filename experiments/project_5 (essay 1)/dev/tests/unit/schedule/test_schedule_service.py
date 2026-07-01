from __future__ import annotations

import pytest
from datetime import datetime
from src.service.schedule.schedule_service import ScheduleService


class TestScheduleService:
    def setup_method(self) -> None:
        self.service = ScheduleService()

    def test_is_exam_accessible_within_window(self) -> None:
        result = self.service.is_exam_accessible(
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
            current_time=datetime(2024, 6, 1, 12, 0, 0),
        )
        assert result is True

    def test_is_exam_accessible_outside_window(self) -> None:
        result = self.service.is_exam_accessible(
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
            current_time=datetime(2024, 5, 31, 23, 59, 59),
        )
        assert result is False

    def test_get_time_limit_seconds_with_limit(self) -> None:
        result = self.service.get_time_limit_seconds(60)
        assert result == 3600

    def test_get_time_limit_seconds_no_limit(self) -> None:
        result = self.service.get_time_limit_seconds(None)
        assert result is None
