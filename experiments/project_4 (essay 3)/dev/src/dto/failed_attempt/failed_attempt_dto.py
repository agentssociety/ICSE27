from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class FailedAttemptBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FailedAttemptCreate(FailedAttemptBase):
    operation: str


class FailedAttemptUpdate(FailedAttemptBase):
    operation: Optional[str] = None


class FailedAttemptResponse(FailedAttemptBase):
    id: int
    operation: str
