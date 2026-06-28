from __future__ import annotations

import pytest
from uuid import uuid4

from src.domain.patient import Patient, RecordState, SeverityLevel, SymptomResource


def test_create_patient_creates_new_patient() -> None:
    """createPatient creates a new Patient instance with the given symptoms."""
    patient = Patient()
    result = patient.createPatient(name="John Doe", symptoms=["fever", "cough"])
    assert result is not None
    assert isinstance(result, Patient)
    assert result.state == RecordState.PENDING_TRIAGE
    assert result.urgency_level == 99


def test_create_patient_has_unique_id() -> None:
    """Each call to createPatient generates a unique patientId."""
    patient = Patient()
    p1 = patient.createPatient(name="Alice", symptoms=["headache"])
    p2 = patient.createPatient(name="Bob", symptoms=["chest pain"])
    assert p1.patientId != p2.patientId


def test_patient_default_state_is_pending_triage() -> None:
    """A new Patient defaults to PENDING_TRIAGE state."""
    p = Patient()
    assert p.state == RecordState.PENDING_TRIAGE


def test_patient_default_urgency_is_99() -> None:
    """A new Patient defaults to urgency_level 99 (not yet triaged)."""
    p = Patient()
    assert p.urgency_level == 99


def test_patient_can_be_added_to_queue() -> None:
    """A patient can be assigned to a patient queue."""
    from src.domain.patient_queue import PatientQueue
    queue = PatientQueue()
    p = Patient(patientQueue=queue)
    assert p.patientQueue is queue
