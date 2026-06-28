from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from enum import Enum


"""
Domain layer for the TransfusionRequest domain class

Package: domain.transfusion_request
Layer: domain
Related tasks: #33, #34, #35, #38
Requirement coverage:
- Accept and Store Transfusion Requests
- Exact ABO/Rh Match First
- Automated Blood Unit Reservation and Release
- Dashboard displaying current stock levels, expiration warnings, and transfusion requests
"""


class RequestState(Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    STORED = "stored"
    FAILED = "failed"


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


class RhFactorType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


@dataclass
class TransfusionRequest:
    bloodType: str
    rhFactor: str
    quantity: int
    state: RequestState = RequestState.PENDING


@dataclass
class TransfusionRequestId:
    request_id: str


@dataclass
class TransfusionRequestCreatedEvent:
    request_id: str
    blood_type: str
    rh_factor: str
    quantity: int


@dataclass
class TransfusionRequestUpdatedEvent:
    request_id: str
    new_state: RequestState
