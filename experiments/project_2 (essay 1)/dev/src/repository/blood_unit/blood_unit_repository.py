from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.blood_unit import ABO, BloodUnit, Rh

"""
Repository layer for the BloodUnit domain class

Package: repository.blood_unit
Layer: repository
Related tasks: #25, #27, #28, #29, #30, #31
Requirement coverage:
- Track Blood Units by Type, Rh Factor, and Donation Date
- Blood Unit Compatibility Matching
- Automatic Release of Reserved Units for Scheduled Transfusions
- Automate Expiration of Blood Units Older than 42 Days
- Blood Stock Alert System
"""

class BloodUnitDB(Protocol):
    def store(self, unit: BloodUnit) -> None:
        ...

    def retrieve(self, id: str) -> BloodUnit:
        ...

    def retrieveAll(self) -> list[BloodUnit]:
        ...

    def update(self, unit: BloodUnit) -> None:
        ...

class DateCalculationAPI(Protocol):
    def calculateExpirationDate(self, donationDate: Date, bloodType: ABO, rhFactor: Rh) -> Date:
        ...
