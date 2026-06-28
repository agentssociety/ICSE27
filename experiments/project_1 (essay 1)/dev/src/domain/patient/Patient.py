from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from src.domain.patient_queue import PatientQueue

"""
Domain layer for the Patient domain class

Package: domain.patient
Layer: domain
Related tasks: #1, #2, #3, #4, #5, #6
Requirement coverage:
- Register New Patient with Symptoms
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Dequeue Next Highest-Priority Patient
"""

class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RecordState(Enum):
    PENDING_TRIAGE = "pending_triage"
    IN_CONSULTATION = "in_consultation"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"

class Role(Enum):
    TRIAGE_NURSE_TEAM = "triage_nurse_team"
    MEDICAL_STAFF = "medical_staff"
    PATIENT_CARE_COORDINATION_TEAM = "patient_care_coordination_team"

@dataclass
class SymptomResource:
    patient: Patient

@dataclass
class Patient:
    patientId: UUID = field(default_factory=uuid4)
    symptoms: list[SymptomResource] = field(default_factory=list)
    state: RecordState = RecordState.PENDING_TRIAGE
    patientQueue: PatientQueue | None = None
    arrival_time: datetime = field(default_factory=datetime.now)
    urgency_level: int = 99  # Lower is more urgent; 99 = not yet triaged

    def createPatient(self, name: str, symptoms: list[str]) -> Patient:
        """Create a new patient with the given name and symptoms."""
        patient = Patient(
            patientId=uuid4(),
            symptoms=[SymptomResource(patient=Patient) for s in symptoms],
            state=RecordState.PENDING_TRIAGE,
            arrival_time=datetime.now(),
            urgency_level=99,
        )
        return patient

@dataclass
class PatientId:
    id: UUID

@dataclass
class PatientCreatedEvent:
    patient: Patient

@dataclass
class PatientUpdatedEvent:
    patient: Patient
