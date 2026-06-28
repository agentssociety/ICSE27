from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.blood_unit import BloodUnit
    from src.domain.transfusion_request import TransfusionRequest


class ReservationStatus(Enum):
    ACTIVE = "active"
    RELEASED = "released"
    EXPIRED = "expired"


@dataclass
class Reservation:
    """A reservation of a blood unit for a transfusion request."""
    id: str
    request_id: str
    unit_id: int
    reserved_at: datetime
    timeout_minutes: int = 30
    status: ReservationStatus = ReservationStatus.ACTIVE

    def is_expired(self, current_time: datetime | None = None) -> bool:
        """Check if the reservation has timed out."""
        if current_time is None:
            current_time = datetime.now()
        elapsed = current_time - self.reserved_at
        return elapsed > timedelta(minutes=self.timeout_minutes)

    def release(self) -> None:
        """Release the reservation."""
        self.status = ReservationStatus.RELEASED

    def expire(self) -> None:
        """Mark the reservation as expired."""
        self.status = ReservationStatus.EXPIRED

