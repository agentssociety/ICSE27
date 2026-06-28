from __future__ import annotations

from datetime import date
from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from src.domain.transfusion_request import TransfusionRequest

"""
Domain layer for the BloodUnit domain class

Package: domain.blood_unit
Layer: domain
Related tasks: #32, #34, #35, #36, #37, #38
Requirement coverage:
- Track Blood Units by ABO Type, Rh Factor, Collection Date, and Expiry
- Exact ABO/Rh Match First
- Automated Blood Unit Reservation and Release
- Automated Expiration of Blood Units
- Monitor Blood Inventory Levels and Alert on Low Stock
"""

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

class ABOType(Enum):
    A = "a"
    B = "b"
    AB = "ab"
    O = "o"

class RhFactor(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class BloodUnitStatus(Enum):
    AVAILABLE = "available"
    ISSUED = "issued"
    EXPIRED = "expired"

class State(Enum):
    PRE1 = "pre1"
    PRE2 = "pre2"
    POST1 = "post1"
    POST2 = "post2"
    POST3 = "post3"
    POST4 = "post4"
    POST5 = "post5"

@dataclass
class Actor:
    name: str
    mayPerform: list[Permission]

@dataclass
class BloodUnit:
    uniqueID: str
    aboType: ABOType
    rhFactor: RhFactor
    collectionDate: Date
    expiryDate: Date
    status: BloodUnitStatus

@dataclass
class Resource:
    owner: Actor
    accessible: list[Actor]

@dataclass
class BloodUnitId:
    pass

@dataclass
class BloodUnitCreatedEvent:
    pass

@dataclass
class BloodUnitUpdatedEvent:
    pass
