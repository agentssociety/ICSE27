from __future__ import annotations

import pytest
from uuid import uuid4

from src.domain.patient import Patient, RecordState
from src.domain.patient_queue import PatientQueue
from src.service.patient.patient_service import PatientServiceImpl


@pytest.fixture
def service() -> PatientServiceImpl:
    return PatientServiceImpl()


@pytest.fixture
def queue() -> PatientQueue:
    return PatientQueue()


def test_register_patient_adds_to_queue(service: PatientServiceImpl, queue: PatientQueue) -> None:
    """register_patient adds the patient to the queue."""
    patient = service.register_patient(name="John Doe", symptoms=["fever", "cough"], queue=queue)
    assert patient in queue.patients
    assert len(queue.patients) == 1


def test_register_patient_creates_patient_with_pending_state(service: PatientServiceImpl, queue: PatientQueue) -> None:
    """register_patient creates a patient with PENDING_TRIAGE state."""
    patient = service.register_patient(name="Jane", symptoms=["headache"], queue=queue)
    assert patient.state == RecordState.PENDING_TRIAGE


def test_register_patient_sets_urgency_to_99(service: PatientServiceImpl, queue: PatientQueue) -> None:
    """register_patient sets urgency_level to 99 (not yet triaged)."""
    patient = service.register_patient(name="Bob", symptoms=["chest pain"], queue=queue)
    assert patient.urgency_level == 99


def test_register_patient_returns_patient(service: PatientServiceImpl, queue: PatientQueue) -> None:
    """register_patient returns the created Patient."""
    patient = service.register_patient(name="Alice", symptoms=["fever"], queue=queue)
    assert isinstance(patient, Patient)
    assert patient.patientId is not None
