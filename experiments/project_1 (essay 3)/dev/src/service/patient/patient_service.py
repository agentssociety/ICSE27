from __future__ import annotations

from typing import Any, Protocol
from dataclasses import dataclass

"""
Service layer for the Patient domain class

Package: service.patient
Layer: service
Related tasks: #53, #54, #55, #56, #57, #58
Requirement coverage:
- Register Symptoms
- Assign Item Urgency Level
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
"""

from src.domain.patient.Patient import Patient, SymptomRecord, UserAuthenticationSystem


class SymptomRegistrationService(Protocol):
    """Handles symptom registration workflow."""
    def register_symptom(self, username: str, session_token: str, description: str, language: str) -> SymptomRecord:
        ...


class PatientSymptomService:
    """Implementation of symptom registration service."""

    def __init__(self) -> None:
        self._patients: dict[str, Patient] = {}

    def add_patient(self, patient: Patient) -> None:
        self._patients[patient.username] = patient

    def register_symptom(self, username: str, session_token: str, description: str, language: str) -> SymptomRecord:
        patient = self._patients.get(username)
        if patient is None:
            raise ValueError(f"Patient '{username}' not found")

        # Authenticate
        patient.authentication.authenticate(session_token)

        # Register symptom
        record = patient.inputSymptoms(description, language)
        return record
