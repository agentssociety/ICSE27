from __future__ import annotations

from typing import Any
from dataclasses import dataclass

"""
Dto layer for the Alert domain class

Package: dto.alert
Layer: dto
Related tasks: #30
Requirement coverage:
- Blood Stock Alert System
"""

@dataclass
class AlertRequest:
    targetUsers: list[str]
    message: str
    channels: list[str]

@dataclass
class InventoryLevel:
    bloodType: str
    units: int

@dataclass
class OperationRequest:
    initiatorId: str
    targetResourceIds: list[str]
