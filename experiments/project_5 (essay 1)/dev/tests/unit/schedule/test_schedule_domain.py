from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from src.domain.schedule import Schedule


class TestScheduleDomain:
    def test_is_accessible_within_window(self) -> None:
        now = datetime(2024, 6, 1, 12, 0, 0)
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
        )
        assert schedule.is_accessible(now) is True

    def test_is_accessible_before_window(self) -> None:
        now = datetime(2024, 5, 31, 23, 59, 59)
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
        )
        assert schedule.is_accessible(now) is False

    def test_is_accessible_after_window(self) -> None:
        now = datetime(2024, 6, 2, 0, 0, 1)
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
        )
        assert schedule.is_accessible(now) is False

    def test_is_accessible_exact_open(self) -> None:
        now = datetime(2024, 6, 1, 0, 0, 0)
        schedule = Schedule(
            exam_id="exam1",
            open_date=now,
            close_date=datetime(2024, 6, 2, 0, 0, 0),
        )
        assert schedule.is_accessible(now) is True

    def test_is_accessible_exact_close(self) -> None:
        now = datetime(2024, 6, 2, 0, 0, 0)
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=now,
        )
        assert schedule.is_accessible(now) is True

    def test_get_time_limit_seconds_with_limit(self) -> None:
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
            per_attempt_time_limit_minutes=60,
        )
        assert schedule.get_time_limit_seconds() == 3600

    def test_get_time_limit_seconds_no_limit(self) -> None:
        schedule = Schedule(
            exam_id="exam1",
            open_date=datetime(2024, 6, 1, 0, 0, 0),
            close_date=datetime(2024, 6, 2, 0, 0, 0),
        )
        assert schedule.get_time_limit_seconds() is None
