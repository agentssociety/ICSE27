from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FlaggedTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    withdrawal_id: str
    reason: str
    flagged_at: datetime
    reviewed_by: Optional[str] = None
    status: str


class FlaggedTransactionListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[FlaggedTransactionResponse]
    total: int


class FlagReviewRequest(BaseModel):
    reviewer_id: str

