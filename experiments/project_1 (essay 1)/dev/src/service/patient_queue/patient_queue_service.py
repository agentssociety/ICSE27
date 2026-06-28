from __future__ import annotations

from typing import Any, Protocol
from uuid import UUID

from src.domain.patient_queue import PatientQueue
from src.domain.patient import Patient

"""
Service layer for the PatientQueue domain class

Package: service.patient_queue
Layer: service
Related tasks: #1, #3, #4, #5, #6
Requirement coverage:
- Register New Patient with Symptoms
- Sort Patient Queue by Urgency and Arrival Time
- Automated Queue Re-sorting upon Patient Registration or Urgency Update
- Dequeue Next Highest-Priority Patient
- Real-time Patient Dashboard
"""


class PatientQueueService(Protocol):
    def sort_queue(self, queue: PatientQueue) -> list[Patient]:
        """Sort the queue by urgency (highest first) then arrival time (earliest first)."""
        ...

    def get_next_patient(self, queue: PatientQueue) -> Patient | None:
        """Get the highest-priority patient without removing them."""
        ...

    def dequeue_next(self, queue: PatientQueue) -> Patient | None:
        """Remove and return the highest-priority patient."""
        ...


class PatientQueueServiceImpl:
    def __init__(self) -> None:
        pass

    def sort_queue(self, queue: PatientQueue) -> list[Patient]:
        """Sort the queue by urgency (highest first) then arrival time (earliest first)."""
        sorted_patients = queue.sortByUrgencyAndArrival()
        queue.updateOrder(sorted_patients)
        return sorted_patients

    def get_next_patient(self, queue: PatientQueue) -> Patient | None:
        """Get the highest-priority patient without removing them."""
        if not queue.patients:
            return None
        sorted_patients = queue.sortByUrgencyAndArrival()
        return sorted_patients[0]

    def dequeue_next(self, queue: PatientQueue) -> Patient | None:
        """Remove and return the highest-priority patient."""
        if not queue.patients:
            return None
        sorted_patients = queue.sortByUrgencyAndArrival()
        next_patient = sorted_patients[0]
        queue.patients.remove(next_patient)
        return next_patient
