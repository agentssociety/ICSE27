from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4

"""
Domain layer for the TransfusionRequest domain class

Package: domain.transfusion_request
Layer: domain
Related tasks: #26, #27, #31
Requirement coverage:
- Accept and Log Transfusion Requests
- Blood Unit Compatibility Matching
- Inventory Dashboard Display
"""


class StateEnum(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    MATCHING = "matching"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


@dataclass
class PatientDetails:
    name: str
    dateOfBirth: str
    medicalRecordNumber: str
    transfusionRequest: Optional[TransfusionRequest] = None  # Forward ref, set later

    def __post_init__(self) -> None:
        """Validate patient details."""
        if not self.name or not self.name.strip():
            raise ValueError("Patient name cannot be empty")
        if not self.medicalRecordNumber or not self.medicalRecordNumber.strip():
            raise ValueError("Medical record number cannot be empty")

    def updateDetails(self, name: Optional[str] = None, dateOfBirth: Optional[str] = None,
                      medicalRecordNumber: Optional[str] = None) -> None:
        """Update patient details."""
        if name is not None:
            if not name.strip():
                raise ValueError("Patient name cannot be empty")
            self.name = name
        if dateOfBirth is not None:
            self.dateOfBirth = dateOfBirth
        if medicalRecordNumber is not None:
            if not medicalRecordNumber.strip():
                raise ValueError("Medical record number cannot be empty")
            self.medicalRecordNumber = medicalRecordNumber


@dataclass
class BloodType:
    type: str
    transfusionRequest: Optional[TransfusionRequest] = None

    def __post_init__(self) -> None:
        """Validate blood type."""
        valid_types = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
        if self.type not in valid_types:
            raise ValueError(f"Invalid blood type: {self.type}. Must be one of {valid_types}")


@dataclass
class Quantity:
    units: int
    transfusionRequest: Optional[TransfusionRequest] = None

    def __post_init__(self) -> None:
        """Validate quantity."""
        if self.units <= 0:
            raise ValueError("Quantity must be positive")
        if self.units > 100:
            raise ValueError("Quantity exceeds maximum allowed (100 units)")


@dataclass
class Urgency:
    level: str
    transfusionRequest: Optional[TransfusionRequest] = None

    def __post_init__(self) -> None:
        """Validate urgency level."""
        valid_levels = {"low", "medium", "high", "critical"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid urgency level: {self.level}. Must be one of {valid_levels}")


@dataclass
class UniqueID:
    id: UUID

    @classmethod
    def generate(cls) -> UniqueID:
        """Generate a new unique ID."""
        return cls(id=uuid4())


@dataclass
class TransfusionRequest:
    uniqueID: UniqueID
    patientDetails: PatientDetails
    bloodType: BloodType
    quantity: Quantity
    urgency: Urgency
    state: StateEnum = StateEnum.PENDING
    duplicateFlag: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate invariants."""
        # Invariant: set back-reference on child objects
        self.patientDetails.transfusionRequest = self
        self.bloodType.transfusionRequest = self
        self.quantity.transfusionRequest = self
        self.urgency.transfusionRequest = self

        # Invariant: duplicate checking
        if self.duplicateFlag:
            raise ValueError("Duplicate transfusion request detected")

    def isDuplicate(self, other: TransfusionRequest) -> bool:
        """Check if this request is a duplicate of another."""
        return (
            self.patientDetails.medicalRecordNumber == other.patientDetails.medicalRecordNumber
            and self.bloodType.type == other.bloodType.type
            and self.quantity.units == other.quantity.units
        )

    def updateState(self, new_state: StateEnum) -> None:
        """Update the state of the transfusion request with validation."""
        valid_transitions = {
            StateEnum.PENDING: [StateEnum.APPROVED, StateEnum.CANCELLED],
            StateEnum.APPROVED: [StateEnum.MATCHING, StateEnum.CANCELLED],
            StateEnum.MATCHING: [StateEnum.FULFILLED, StateEnum.CANCELLED],
            StateEnum.FULFILLED: [],
            StateEnum.CANCELLED: [],
        }
        if self.state not in valid_transitions:
            raise ValueError(f"Current state {self.state.value} has no valid transitions")
        if new_state not in valid_transitions[self.state]:
            raise ValueError(
                f"Invalid state transition from {self.state.value} to {new_state.value}"
            )
        self.state = new_state
        self.updated_at = datetime.now()

    def canFulfill(self, available_units: int) -> bool:
        """Check if the request can be fulfilled with available units."""
        return self.state == StateEnum.MATCHING and available_units >= self.quantity.units


@dataclass
class TransfusionRequestId:
    """Value Object for Transfusion Request ID."""
    id: str


@dataclass
class TransfusionRequestCreatedEvent:
    """Event raised when a TransfusionRequest is created."""
    request_id: TransfusionRequestId
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TransfusionRequestUpdatedEvent:
    """Event raised when a TransfusionRequest is updated."""
    request_id: TransfusionRequestId
    timestamp: datetime = field(default_factory=datetime.now)
