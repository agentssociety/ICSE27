from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

"""
Domain layer for the Patient domain class

Package: domain.patient
Layer: domain
Related tasks: #7, #8, #9, #10, #11, #12
Requirement coverage:
- Register New Patient with Symptoms
- Assign Urgency Level to Patient
- Sort Patient Queue by Urgency and Arrival Time
- Queue Reordering on Patient Addition and Urgency Change
- Take Next Patient from Sorted Queue
"""


@dataclass(eq=True, frozen=True)
class Actor:
    mayPerform: set[Permission]

    def __hash__(self) -> int:
        return id(self)

    def checkPermission(self, actorId: str, requiredPermission: Permission) -> bool:
        return requiredPermission in self.mayPerform


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"


@dataclass
class PatientRecord:
    owner: Actor
    accessible: set[Actor]

    def createPatientRecord(self, patientData: dict) -> PatientRecord:
        return PatientRecord(owner=self.owner, accessible=self.accessible)


@dataclass
class SymptomData:
    owner: Actor
    accessible: set[Actor]

    def createSymptomData(self, symptoms: str, patientId: str) -> SymptomData:
        return SymptomData(owner=self.owner, accessible=self.accessible)


@dataclass
class QueueEntry:
    owner: Actor
    accessible: set[Actor]

    def createQueueEntry(self, patientId: str, status: str) -> QueueEntry:
        return QueueEntry(owner=self.owner, accessible=self.accessible)


@dataclass
class DataAtRestEncryption:
    resource: Resource
    encrypted: bool

    def encryptResource(self, resource: Resource) -> None:
        self.resource = resource
        self.encrypted = True


@dataclass
class Resource:
    owner: Actor
    accessible: set[Actor]


@dataclass
class Patient:
    symptoms: str
    urgencyLevel: int  # 1..5
    queuePosition: int
    arrivalTime: datetime
    urgency: str

    def assignUrgency(self, level: int) -> None:
        if level < 1 or level > 5:
            raise ValueError(f"Urgency level must be between 1 and 5, got {level}")
        self.urgencyLevel = level
        self.urgency = str(level)

    def updateUrgency(self, newUrgencyLevel: str) -> None:
        self.urgency = newUrgencyLevel

    def getDetails(self) -> dict:
        return {
            "symptoms": self.symptoms,
            "urgencyLevel": self.urgencyLevel,
            "queuePosition": self.queuePosition,
            "arrivalTime": self.arrivalTime.isoformat(),
            "urgency": self.urgency,
        }


@dataclass
class PatientId:
    value: str = ""


@dataclass
class PatientCreatedEvent:
    patientId: str = ""


@dataclass
class PatientUpdatedEvent:
    patientId: str = ""
