from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from enum import Enum

"""
Domain layer for the TransactionState domain class

Package: domain.transaction_state
Layer: domain
Related tasks: None
"""

class TransactionState(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class TransactionStateId:
    pass

@dataclass
class TransactionStateCreatedEvent:
    pass

@dataclass
class TransactionStateUpdatedEvent:
    pass
