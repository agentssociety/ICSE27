from __future__ import annotations

import pytest
from uuid import UUID
from datetime import date
from src.service.attempt_review.attempt_review_service import (
    PastAttemptData, DashboardData, TrendData, Attempt, ChartPoint,
    ReviewService, AccessControlService, Permission, Role
)
from src.domain.student import Student


class TestAttemptData:
    def test_past_attempt_data_creation(self) -> None:
        data = PastAttemptData(studentId=UUID("12345678-1234-5678-1234-567812345678"))
        assert data.studentId is not None

    def test_verify_access_matching_student(self) -> None:
        student = Student(id="00000000-0000-0000-0000-000000000000", name="Test", email="test@test.com")
        data = PastAttemptData(studentId=UUID("00000000-0000-0000-0000-000000000000"))
        assert data.verifyAccess(student) is True

    def test_verify_access_no_student_id(self) -> None:
        student = Student(id="some_id", name="Test", email="test@test.com")
        data = PastAttemptData()
        assert data.verifyAccess(student) is True


class TestDashboardData:
    def test_create_from_attempts_empty(self) -> None:
        data = DashboardData()
        result = data.createFromAttempts([])
        assert result.overallProgress == 0.0

    def test_create_from_attempts_with_scores(self) -> None:
        data = DashboardData()
        atts = [Attempt(score=80.0), Attempt(score=90.0)]
        result = data.createFromAttempts(atts)
        assert result.overallProgress == 85.0

    def test_verify_access_always_true(self) -> None:
        data = DashboardData()
        assert data.verifyAccess(None) is True
