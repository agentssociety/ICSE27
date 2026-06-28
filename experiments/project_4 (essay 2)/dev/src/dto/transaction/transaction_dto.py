from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

"""
Dto layer for the Transaction domain class

Package: dto.transaction
Layer: dto
Related tasks: #90, #92, #93
Requirement coverage:
- Enforce daily transaction limits
- Detect Suspicious Transaction Patterns
- Admin Interface for Flagged Transactions Review
"""


class TransactionCreateRequest(BaseModel):
    amount: Decimal
    accountId: str
    userId: str


class TransactionUpdateRequest(BaseModel):
    amount: Optional[Decimal] = None
    status: Optional[str] = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    amount: Decimal
    timestamp: datetime
    accountId: str
    status: str
    userId: str
