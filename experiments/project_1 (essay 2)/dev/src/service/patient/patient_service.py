from __future__ import annotations

from typing import Optional, Protocol
from datetime import datetime, timezone

from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse
from src.infra.patient.patient_repo_impl import SQLAlchemyPatientRepository


class PatientService(Protocol):
    """Service interface for patient operations."""

    def register_patient_with_symptoms(self, symptoms: str) -> PatientResponse:
        """Register a new patient with their symptoms and add to evaluation queue."""
        ...

    def assign_urgency(self, patient_id: int, level: int) -> PatientResponse:
        """Assign an urgency level (1-5) to an existing patient."""
        ...

    def get_sorted_queue(self) -> list[PatientResponse]:
        """Get all patients sorted by urgency (asc) then arrival time (asc)."""
        ...

    def reorder_queue(self) -> None:
        """Re-order the entire patient queue based on urgency then arrival time."""
        ...

    def take_next_patient(self) -> PatientResponse:
        """Return the most urgent patient and remove them from the queue."""
        ...


class PatientServiceImpl:
    """Implementation of PatientService."""

    def __init__(self, repository: SQLAlchemyPatientRepository) -> None:
        self._repository = repository

    def register_patient_with_symptoms(self, symptoms: str) -> PatientResponse:
        """Register a new patient with symptoms and add to queue."""
        now = datetime.now(timezone.utc)
        data = PatientCreate(
            symptoms=symptoms,
            urgencyLevel=5,
            queuePosition=0,
            arrivalTime=now,
            urgency="5",
        )
        result = self._repository.create(data)
        self.reorder_queue()
        return result

    def assign_urgency(self, patient_id: int, level: int) -> PatientResponse:
        """Assign an urgency level (1-5) to an existing patient."""
        if level < 1 or level > 5:
            raise ValueError(f"Urgency level must be between 1 and 5, got {level}")
        update_data = PatientUpdate(urgencyLevel=level, urgency=str(level))
        result = self._repository.update(patient_id, update_data)
        if result is None:
            raise ValueError(f"Patient with id {patient_id} not found")
        self.reorder_queue()
        return result

    def get_sorted_queue(self) -> list[PatientResponse]:
        """Get all patients sorted by urgency (asc) then arrival time (asc)."""
        all_patients = self._repository.get_all(skip=0, limit=10000)
        return sorted(all_patients, key=lambda p: (p.urgencyLevel, p.arrivalTime))

    def reorder_queue(self) -> None:
        """Re-order the entire patient queue based on urgency then arrival time."""
        sorted_patients = self.get_sorted_queue()
        for position, patient in enumerate(sorted_patients):
            if patient.queuePosition != position:
                update_data = PatientUpdate(queuePosition=position)
                self._repository.update(patient.id, update_data)

    def take_next_patient(self) -> PatientResponse:
        """Return the most urgent patient and remove them from the queue."""
        queue = self.get_sorted_queue()
        if not queue:
            raise IndexError("No patients in the queue")
        patient = queue[0]
        self._repository.delete(patient.id)
        self.reorder_queue()
        return patient
