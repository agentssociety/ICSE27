from __future__ import annotations

from typing import Any, Protocol
from datetime import datetime
from uuid import UUID

from src.domain.patient_queue import PatientQueue
from src.domain.patient import Patient
from src.domain.urgency_level import UrgencyLevel, urgency_to_int

"""
Service layer for the Dashboard domain class

Package: service.dashboard
Layer: service
Related tasks: #6
Requirement coverage:
- Real-time Patient Dashboard
"""


class PatientDashboardInfo:
    """Data transfer object for patient dashboard information."""
    def __init__(
        self,
        patient_id: UUID,
        urgency_level: str,
        urgency_sort_order: int,
        arrival_time: datetime,
        estimated_wait_minutes: int,
    ) -> None:
        self.patient_id = patient_id
        self.urgency_level = urgency_level
        self.urgency_sort_order = urgency_sort_order
        self.arrival_time = arrival_time
        self.estimated_wait_minutes = estimated_wait_minutes


class DashboardService(Protocol):
    def get_queue_overview(self, queue: PatientQueue) -> list[PatientDashboardInfo]:
        """Get a complete overview of the queue for the dashboard."""
        ...

    def calculate_estimated_wait(self, patient: Patient, queue: PatientQueue) -> int:
        """Calculate estimated wait time in minutes for a given patient."""
        ...


class DashboardServiceImpl:
    def __init__(self) -> None:
        pass

    def get_queue_overview(self, queue: PatientQueue) -> list[PatientDashboardInfo]:
        """Get a complete overview of the queue for the dashboard."""
        sorted_patients = queue.sortByUrgencyAndArrival()
        overview = []
        for patient in sorted_patients:
            wait_minutes = self.calculate_estimated_wait(patient, queue)
            urgency_name = self._urgency_level_name(patient.urgency_level)
            info = PatientDashboardInfo(
                patient_id=patient.patientId,
                urgency_level=urgency_name,
                urgency_sort_order=patient.urgency_level,
                arrival_time=patient.arrival_time,
                estimated_wait_minutes=wait_minutes,
            )
            overview.append(info)
        return overview

    def calculate_estimated_wait(self, patient: Patient, queue: PatientQueue) -> int:
        """Calculate estimated wait time in minutes for a given patient.
        
        Simple heuristic: each patient ahead in priority takes ~15 minutes.
        """
        sorted_patients = queue.sortByUrgencyAndArrival()
        position = 0
        for i, p in enumerate(sorted_patients):
            if p.patientId == patient.patientId:
                position = i
                break
        else:
            return 0  # Patient not found in queue
        return position * 15  # 15 minutes per patient ahead

    def _urgency_level_name(self, urgency_level: int) -> str:
        """Convert numeric urgency level to human-readable name."""
        mapping = {
            0: "CRITICAL",
            1: "HIGH",
            2: "MEDIUM",
            3: "LOW",
        }
        return mapping.get(urgency_level, "UNKNOWN")
