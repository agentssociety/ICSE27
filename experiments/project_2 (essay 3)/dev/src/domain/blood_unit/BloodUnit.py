from __future__ import annotations

from datetime import date
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.reservation import Reservation


@dataclass
class BloodUnit:
    """A unit of blood tracked in the inventory."""
    abo_rh_type: str
    collection_date: date
    id: int | None = None
    has_complete_data: bool = True
    is_expired: bool = False
    reservations: list[Reservation] = field(default_factory=list)

    def mark_expired(self) -> None:
        self.is_expired = True

    def __post_init__(self) -> None:
        if self.abo_rh_type not in ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"):
            raise ValueError(f"Invalid ABO/Rh type: {self.abo_rh_type}")

