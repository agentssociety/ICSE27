from __future__ import annotations

import pytest
from uuid import UUID
from src.service.competency_trend_chart.competency_trend_chart_service import (
    PastAttemptData, DashboardData, TrendData, Attempt, ChartPoint,
    ReviewService, AccessControlService, Permission, Role
)
from src.domain.student import Student


class TestDataClasses:
    def test_past_attempt_defaults(self) -> None:
        data = PastAttemptData()
        assert data.studentId is None
        assert data.attempts is None

    def test_dashboard_defaults(self) -> None:
        data = DashboardData()
        assert data.overallProgress is None

    def test_trend_defaults(self) -> None:
        data = TrendData()
        assert data.trendDirection is None
        assert data.sufficientData is None

    def test_enums_exist(self) -> None:
        assert Permission.READ.value == "read"
        assert Role.STUDENT.value == "student"
