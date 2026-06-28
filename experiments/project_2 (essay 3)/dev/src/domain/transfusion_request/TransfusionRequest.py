from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.blood_unit import BloodUnit
    from src.domain.reservation import Reservation


class RequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class TransfusionRequest:
    """A transfusion request submitted by medical staff."""
    request_id: str
    patient_id: str
    patient_abo_rh: str
    blood_type: str
    request_date: date
    status: RequestStatus = RequestStatus.PENDING
    matched_units: list[str] = field(default_factory=list)
    excluded_units: list[str] = field(default_factory=list)
    reservations: list[Reservation] = field(default_factory=list)

    def accept(self) -> None:
        """Accept the transfusion request."""
        self.status = RequestStatus.ACCEPTED

    def process(self) -> None:
        """Mark request as being processed."""
        self.status = RequestStatus.PROCESSING

    def complete(self) -> None:
        """Mark request as completed."""
        self.status = RequestStatus.COMPLETED

    def cancel(self) -> None:
        """Cancel the request."""
        self.status = RequestStatus.CANCELLED

