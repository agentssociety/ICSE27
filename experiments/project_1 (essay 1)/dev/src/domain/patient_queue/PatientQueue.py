from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from src.domain.patient import Patient
    from src.domain.urgency_level import UrgencyLevel

"""
Domain layer for the PatientQueue domain class

Package: domain.patient_queue
Layer: domain
Related tasks: #1, #3, #4, #5, #6
Requirement coverage:
- Register New Patient with Symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Dequeue Next Highest-Priority Patient
- Real-time Patient Dashboard
"""


class QueueState(Enum):
    PRE_SORT = "pre_sort"
    POST_SORT = "post_sort"


def _urgency_sort_key(patient: Patient) -> tuple[int, datetime]:
    """Sort key: lower urgency_level (more urgent) first, then earlier arrival_time first."""
    return (patient.urgency_level, patient.arrival_time)


@dataclass
class PatientQueue:
    queueId: UUID = field(default_factory=uuid4)
    patients: list[Patient] = field(default_factory=list)
    state: QueueState = QueueState.PRE_SORT
    urgencyLevel: Optional[UrgencyLevel] = None

    def readAllPatients(self) -> list[Patient]:
        return list(self.patients)

    def updateOrder(self, sortedPatients: list[Patient]) -> None:
        self.patients = sortedPatients
        self.state = QueueState.POST_SORT

    def sortByUrgencyAndArrival(self) -> list[Patient]:
        """Return patients sorted by urgency (highest first) then arrival time (earliest first)."""
        return sorted(self.patients, key=_urgency_sort_key)

    def checkForUrgencyChange(self, originalUrgencies: dict[UUID, int]) -> bool:
        """Check if any patient's urgency level changed from the original map."""
        for patient in self.patients:
            if patient.patientId in originalUrgencies:
                if patient.urgency_level != originalUrgencies[patient.patientId]:
                    return True
            else:
                return True
        return False

    def failure(self, e_g: Any, connection_lost: Any) -> None:
        pass

    def error(self, e_g: Any, timeout: Any) -> None:
        pass


@dataclass
class PatientQueueId:
    id: UUID


@dataclass
class PatientQueueCreatedEvent:
    queue: PatientQueue


@dataclass
class PatientQueueUpdatedEvent:
    queue: PatientQueue
