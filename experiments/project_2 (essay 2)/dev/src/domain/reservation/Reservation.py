from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.blood_unit import BloodUnit
    from src.domain.transfusion_request import TransfusionRequest


"""
Domain layer for the Reservation domain class

Package: domain.reservation
Layer: domain
Related tasks: #35
Requirement coverage:
- Automated Blood Unit Reservation and Release
"""

class BloodUnitStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    ISSUED = "issued"

class TransfusionRequestStatus(Enum):
    PENDING = "pending"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"

class ReservationStatus(Enum):
    ACTIVE = "active"
    RELEASED = "released"
    ISSUED = "issued"

class BloodType(Enum):
    A_POS = "a_pos"
    A_NEG = "a_neg"
    B_POS = "b_pos"
    B_NEG = "b_neg"
    AB_POS = "ab_pos"
    AB_NEG = "ab_neg"
    O_POS = "o_pos"
    O_NEG = "o_neg"

class Role(Enum):
    CLINICAL_STAFF = "clinical_staff"
    BLOOD_BANK_MANAGEMENT = "blood_bank_management"
    IT_TEAM = "it_team"

class Permission(Enum):
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass
class Reservation:
    id: str
    bloodUnitId: str
    transfusionRequestId: str
    reservationTimestamp: datetime
    expiryTimestamp: datetime
    status: ReservationStatus

    def release(self) -> None:
        """Release the reservation, making the blood unit available again."""
        self.status = ReservationStatus.RELEASED

    def is_expired(self) -> bool:
        """Check if the reservation has passed its expiry timestamp."""
        return datetime.now() >= self.expiryTimestamp

    def issue(self) -> None:
        """Mark the reservation as issued."""
        self.status = ReservationStatus.ISSUED


@dataclass
class ReservationId:
    value: str


@dataclass
class ReservationCreatedEvent:
    reservation_id: str
    blood_unit_id: str
    transfusion_request_id: str


@dataclass
class ReservationUpdatedEvent:
    reservation_id: str
    new_status: ReservationStatus
