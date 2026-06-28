from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.blood_unit import ABO, BloodUnit, Rh
    from src.repository.blood_unit import BloodUnitDB, DateCalculationAPI

"""
Service layer for the BloodUnit domain class

Package: service.blood_unit
Layer: service
Related tasks: #25, #27, #28, #29, #30, #31
Requirement coverage:
- Track Blood Units by Type, Rh Factor, and Donation Date
- Blood Unit Compatibility Matching
- Automatic Release of Reserved Units for Scheduled Transfusions
- Automate Expiration of Blood Units Older than 42 Days
- Blood Stock Alert System
"""

class BloodUnitService(Protocol):
    def recordBloodUnit(self, bloodType: ABO, rhFactor: Rh, donationDate: Date) -> BloodUnit:
        ...

    def calculateExpiration(self, unitId: str) -> Date:
        ...

    def flagExpiringUnits(self) -> list[BloodUnit]:
        ...
