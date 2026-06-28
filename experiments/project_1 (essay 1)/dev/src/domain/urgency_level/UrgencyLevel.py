from __future__ import annotations

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from src.domain.patient import Patient

"""
Domain layer for the UrgencyLevel domain class

Package: domain.urgency_level
Layer: domain
Related tasks: #2, #3, #4, #6
Requirement coverage:
- Assign urgency level to patients based on symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Real-time Patient Dashboard
"""


URGENCY_ORDER: dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def urgency_to_int(level: str) -> int:
    """Convert urgency level string to integer for sorting (lower = more urgent)."""
    return URGENCY_ORDER.get(level, 99)


@dataclass
class PatientRecord:
    owner: TriageNurse
    accessible: set[MedicalStaff | PatientCareTeam]

    def updateRecord(self, urgency: Any, priority: Any) -> None:
        pass

    def failure(self, database_timeout: Any) -> None:
        pass


@dataclass
class TriageNurse:
    permissions: Permission
    patients: list[Patient] = field(default_factory=list)


@dataclass
class MedicalStaff:
    permissions: Permission

    def notify(self, patient_ID: Any, priority: Any) -> None:
        pass


@dataclass
class PatientCareTeam:
    permissions: Permission


@dataclass
class HealthcareFacilityManagement:
    permissions: Permission


class PriorityStatus(Enum):
    HIGHEST = "highest"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    LOWEST = "lowest"


class Permission(Enum):
    READ = "read"
    WRITE = "write"


class UrgencyLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def sort_order(self) -> int:
        return URGENCY_ORDER[self.value]


@dataclass
class UrgencyLevelId:
    id: str


@dataclass
class UrgencyLevelCreatedEvent:
    level: UrgencyLevel


@dataclass
class UrgencyLevelUpdatedEvent:
    level: UrgencyLevel
