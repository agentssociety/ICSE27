from __future__ import annotations

from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

"""
Domain layer for the Patient domain class

Package: domain.patient
Layer: domain
Related tasks: #53, #54, #55, #56, #57, #58
Requirement coverage:
- Register Symptoms
- Assign Item Urgency Level
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
"""


@dataclass
class UserAuthenticationSystem:
    sessionToken: str
    userId: str
    patient: Patient  # type: ignore # forward reference

    def authenticate(self, sessionToken: str) -> str:
        if self.sessionToken == sessionToken:
            return self.userId
        raise PermissionError("Invalid session token")


@dataclass
class Symptom:
    description: str
    language: str
    timestamp: datetime
    patientId: str
    patient: Patient  # type: ignore # forward reference

    @staticmethod
    def create(description: str, language: str, patientId: str, patient: Patient) -> Symptom:  # type: ignore
        return Symptom(
            description=description,
            language=language,
            timestamp=datetime.now(),
            patientId=patientId,
            patient=patient,
        )


@dataclass
class SymptomRecord:
    recordId: str
    symptomData: str
    patientId: str
    storedAt: datetime
    symptom: Symptom

    @staticmethod
    def mapToRecord(symptom: Symptom) -> SymptomRecord:
        return SymptomRecord(
            recordId=str(id(symptom)),
            symptomData=f"{symptom.description} [{symptom.language}]",
            patientId=symptom.patientId,
            storedAt=datetime.now(),
            symptom=symptom,
        )

    def setEncryptedAtRest(self) -> None:
        # Placeholder for encryption logic
        pass


@dataclass
class Patient:
    username: str
    authentication: UserAuthenticationSystem

    def inputSymptoms(self, description: str, language: str) -> SymptomRecord:
        symptom = Symptom.create(
            description=description,
            language=language,
            patientId=self.authentication.userId,
            patient=self,
        )
        record = SymptomRecord.mapToRecord(symptom)
        return record

    def displayConfirmation(self, Symptoms_recorded_successfully: Any) -> None:
        pass

    def displayMessage(self, message: Any) -> None:
        pass

    def displayError(self, error_message: Any) -> None:
        pass

    def retryOnReconnection(self) -> None:
        pass


class Permission(Enum):
    WRITE = "write"
    READ = "read"
    ADMIN = "admin"


class SymptomState(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"
    NETWORK_FAILURE = "network_failure"


@dataclass
class PatientId:
    pass


@dataclass
class PatientCreatedEvent:
    pass


@dataclass
class PatientUpdatedEvent:
    pass
