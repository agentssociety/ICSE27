from __future__ import annotations

from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, date, timedelta

"""
Domain layer for the BloodUnit domain class

Package: domain.blood_unit
Layer: domain
Related tasks: #25, #27, #28, #29, #30, #31
Requirement coverage:
- Track Blood Units by Type, Rh Factor, and Donation Date
- Blood Unit Compatibility Matching
- Automatic Release of Reserved Units for Scheduled Transfusions
- Automate Expiration of Blood Units Older than 42 Days
- Blood Stock Alert System
"""


class ABO(Enum):
    A = "a"
    B = "b"
    AB = "ab"
    O = "o"


class Rh(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


# Standard blood unit shelf life: 42 days
BLOOD_UNIT_SHELF_DAYS = 42


@dataclass
class BloodUnit:
    bloodType: ABO
    rhFactor: Rh
    donationDate: date
    expirationDate: Optional[date] = None
    isExpiring: bool = False

    def __post_init__(self) -> None:
        """Initialize calculated fields after dataclass init."""
        if self.expirationDate is None:
            self.expirationDate = self._calculateExpirationDate()
        self._updateExpiringStatus()

    def _calculateExpirationDate(self) -> date:
        """Calculate the expiration date (42 days after donation)."""
        from datetime import timedelta
        return self.donationDate + timedelta(days=BLOOD_UNIT_SHELF_DAYS)

    def _updateExpiringStatus(self) -> None:
        """Update the isExpiring flag if less than 7 days until expiration."""
        if self.expirationDate:
            days_until_expiry = (self.expirationDate - date.today()).days
            self.isExpiring = 0 <= days_until_expiry <= 7

    def getBloodType(self) -> ABO:
        """Get the blood type."""
        return self.bloodType

    def getRhFactor(self) -> Rh:
        """Get the Rh factor."""
        return self.rhFactor

    def getDonationDate(self) -> date:
        """Get the donation date."""
        return self.donationDate

    def setExpirationDate(self, expirationDate: date) -> None:
        """Set a custom expiration date and update status."""
        self.expirationDate = expirationDate
        self._updateExpiringStatus()

    def isExpired(self) -> bool:
        """Check if the blood unit has expired."""
        if self.expirationDate is None:
            return False
        return date.today() > self.expirationDate

    def daysUntilExpiration(self) -> int:
        """Get the number of days until expiration. Negative means expired."""
        if self.expirationDate is None:
            return BLOOD_UNIT_SHELF_DAYS
        return (self.expirationDate - date.today()).days

    def isCompatibleWith(self, recipient_abo: ABO, recipient_rh: Rh) -> bool:
        """Check if this blood unit is compatible with a recipient.
        
        Universal donor rules:
        - O- is universal donor
        - O+ can donate to O+, A+, B+, AB+
        - A can donate to A and AB
        - B can donate to B and AB
        - AB can donate only to AB
        - Rh- can donate to Rh- and Rh+
        - Rh+ can donate only to Rh+
        """
        # Rh compatibility
        if self.rhFactor == Rh.POSITIVE and recipient_rh == Rh.NEGATIVE:
            return False
        
        # ABO compatibility
        if self.bloodType == ABO.O:
            return True  # O is universal donor
        elif self.bloodType == ABO.A:
            return recipient_abo in (ABO.A, ABO.AB)
        elif self.bloodType == ABO.B:
            return recipient_abo in (ABO.B, ABO.AB)
        elif self.bloodType == ABO.AB:
            return recipient_abo == ABO.AB
        
        return False


@dataclass
class BloodUnitId:
    """Value Object for Blood Unit ID."""
    id: str


@dataclass
class BloodUnitCreatedEvent:
    """Event raised when a BloodUnit is created."""
    blood_unit_id: BloodUnitId
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BloodUnitUpdatedEvent:
    """Event raised when a BloodUnit is updated."""
    blood_unit_id: BloodUnitId
    timestamp: datetime = field(default_factory=datetime.now)
