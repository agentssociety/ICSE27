"""Patient model for Hospital Triage Queue System.

This module defines the Patient data class used throughout the application.
It provides a clean interface for patient data with proper type hints and
serialization support.
"""

from datetime import datetime, timezone
from typing import Optional


class Patient:
    """Represents a patient in the triage queue.
    
    Attributes:
        id: Unique identifier for the patient.
        name: Full name of the patient.
        symptoms: Description of symptoms provided by the patient.
        urgency: Triage urgency level from 1 (critical) to 5 (non-urgent).
        triage_time: Timestamp when the patient was last triaged.
        arrival_time: Timestamp when the patient arrived/registered.
        waiting_seconds: Computed waiting time in seconds (not stored).
    """

    def __init__(
        self,
        id: int,
        name: str,
        symptoms: str,
        urgency: int,
        triage_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
    ) -> None:
        """Initialize a new Patient instance.
        
        Args:
            id: Unique patient identifier.
            name: Patient's full name.
            symptoms: Description of symptoms.
            urgency: Urgency level (1-5, where 1 is most urgent).
            triage_time: Time of triage assessment. Defaults to current UTC time.
            arrival_time: Time of arrival. Defaults to current UTC time.
        
        Raises:
            ValueError: If urgency is not in valid range [1, 5].
        """
        if not 1 <= urgency <= 5:
            raise ValueError(
                f"Urgency must be between 1 and 5, got {urgency}"
            )
        
        if not isinstance(id, int) or id < 0:
            raise ValueError(f"id must be a non-negative integer, got {id}")
            
        if not name or not isinstance(name, str):
            raise ValueError("name must be a non-empty string")
            
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("symptoms must be a non-empty string")

        self.id: int = id
        self.name: str = name
        self.symptoms: str = symptoms
        self.urgency: int = urgency
        self.triage_time: datetime = triage_time or datetime.now(timezone.utc)
        self.arrival_time: datetime = arrival_time or datetime.now(timezone.utc)
        
        # Waiting time is computed, not stored
        self.waiting_seconds: int = 0

    def to_dict(self) -> dict:
        """Convert patient data to a dictionary for JSON serialization.
        
        Returns:
            dict: Patient data as a dictionary with all fields.
        """
        return {
            "id": self.id,
            "name": self.name,
            "symptoms": self.symptoms,
            "urgency": self.urgency,
            "triage_time": self.triage_time.isoformat(),
            "arrival_time": self.arrival_time.isoformat(),
            "waiting_seconds": self._compute_waiting_seconds(),
        }

    def _compute_waiting_seconds(self) -> int:
        """Calculate the waiting time in seconds since arrival.
        
        Returns:
            int: Number of seconds since patient arrival.
        """
        now = datetime.now(timezone.utc)
        delta = now - self.arrival_time
        return max(0, int(delta.total_seconds()))

    def __lt__(self, other: "Patient") -> bool:
        """Compare patients for queue ordering.
        
        Patients are ordered by urgency (lower is more urgent) first,
        then by triage time (earlier triage gets priority).
        
        Args:
            other: Another Patient to compare against.
            
        Returns:
            bool: True if this patient has higher priority.
        """
        if not isinstance(other, Patient):
            return NotImplemented
        
        # Lower urgency number means more urgent (priority)
        if self.urgency != other.urgency:
            return self.urgency < other.urgency
        
        # If same urgency, earlier triage time gets priority
        return self.triage_time < other.triage_time

    def __repr__(self) -> str:
        """Return string representation of the patient.
        
        Returns:
            str: Debug representation of the patient.
        """
        return (
            f"Patient(id={self.id}, name='{self.name}', "
            f"urgency={self.urgency})"
        )
