from __future__ import annotations

from typing import Any, Protocol
from uuid import UUID, uuid4
from datetime import datetime

from src.domain.patient import Patient, SymptomResource, RecordState
from src.domain.patient_queue import PatientQueue
from src.domain.urgency_level import UrgencyLevel

"""
Service layer for the Patient domain class

Package: service.patient
Layer: service
Related tasks: #1, #2, #3, #4, #5, #6
Requirement coverage:
- Register New Patient with Symptoms
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Dequeue Next Highest-Priority Patient
"""


class PatientService(Protocol):
    def register_patient(self, name: str, symptoms: list[str], queue: PatientQueue) -> Patient:
        """Register a new patient with symptoms and add to queue."""
        ...

    def assign_urgency(self, patient: Patient, level: UrgencyLevel) -> None:
        """Assign an urgency level to a patient."""
        ...


class PatientServiceImpl:
    def __init__(self) -> None:
        pass

    def register_patient(self, name: str, symptoms: list[str], queue: PatientQueue) -> Patient:
        """Register a new patient with symptoms and add to queue."""
        patient = Patient(
            patientId=uuid4(),
            symptoms=[SymptomResource(patient=Patient) for s in symptoms],
            state=RecordState.PENDING_TRIAGE,
            patientQueue=queue,
            arrival_time=datetime.now(),
            urgency_level=99,
        )
        queue.patients.append(patient)
        return patient

    def assign_urgency(self, patient: Patient, level: UrgencyLevel) -> None:
        """Assign an urgency level to a patient."""
        urgency_map = {
            UrgencyLevel.CRITICAL: 0,
            UrgencyLevel.HIGH: 1,
            UrgencyLevel.MEDIUM: 2,
            UrgencyLevel.LOW: 3,
        }
        patient.urgency_level = urgency_map.get(level, 99)
