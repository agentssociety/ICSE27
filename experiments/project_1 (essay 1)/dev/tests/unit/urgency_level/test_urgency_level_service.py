from __future__ import annotations

import pytest
from uuid import uuid4

from src.domain.patient import Patient
from src.domain.urgency_level import UrgencyLevel
from src.service.urgency_level.urgency_level_service import UrgencyLevelServiceImpl


@pytest.fixture
def service() -> UrgencyLevelServiceImpl:
    return UrgencyLevelServiceImpl()


@pytest.fixture
def patient() -> Patient:
    return Patient()


class TestAssignUrgency:
    def test_critical_symptoms_assign_critical(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """Symptoms like cardiac arrest assign CRITICAL urgency."""
        level = service.assign_urgency(patient, ["cardiac arrest", "unconscious"])
        assert level == UrgencyLevel.CRITICAL

    def test_high_symptoms_assign_high(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """Symptoms like chest pain assign HIGH urgency."""
        level = service.assign_urgency(patient, ["chest pain", "difficulty breathing"])
        assert level == UrgencyLevel.HIGH

    def test_medium_symptoms_assign_medium(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """Symptoms like moderate pain assign MEDIUM urgency."""
        level = service.assign_urgency(patient, ["moderate pain", "nausea"])
        assert level == UrgencyLevel.MEDIUM

    def test_low_symptoms_assign_low(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """Mild symptoms assign LOW urgency."""
        level = service.assign_urgency(patient, ["mild rash", "slight cough"])
        assert level == UrgencyLevel.LOW

    def test_critical_overrides_high(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """If any critical symptom is present, assign CRITICAL even with high symptoms."""
        level = service.assign_urgency(patient, ["chest pain", "cardiac arrest"])
        assert level == UrgencyLevel.CRITICAL

    def test_high_overrides_medium(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """If any high symptom is present, assign HIGH even with medium symptoms."""
        level = service.assign_urgency(patient, ["moderate pain", "chest pain"])
        assert level == UrgencyLevel.HIGH

    def test_empty_symptoms_assign_low(self, service: UrgencyLevelServiceImpl, patient: Patient) -> None:
        """Empty symptoms list assigns LOW urgency."""
        level = service.assign_urgency(patient, [])
        assert level == UrgencyLevel.LOW

    def test_get_urgency_sort_value_critical(self, service: UrgencyLevelServiceImpl) -> None:
        """get_urgency_sort_value returns 0 for CRITICAL."""
        assert service.get_urgency_sort_value(UrgencyLevel.CRITICAL) == 0

    def test_get_urgency_sort_value_low(self, service: UrgencyLevelServiceImpl) -> None:
        """get_urgency_sort_value returns 3 for LOW."""
        assert service.get_urgency_sort_value(UrgencyLevel.LOW) == 3
