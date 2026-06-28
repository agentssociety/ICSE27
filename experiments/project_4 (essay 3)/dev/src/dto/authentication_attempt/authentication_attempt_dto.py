from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class AuthenticationAttemptBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthenticationAttemptCreate(AuthenticationAttemptBase):
    user_id: str
    outcome: str = "failure"
    method: str = "login"
    ip_address: str = "0.0.0.0"

    @field_validator('outcome')
    @classmethod
    def validate_outcome(cls, v: str) -> str:
        allowed = {"success", "failure"}
        if v not in allowed:
            raise ValueError(f"Outcome must be one of {allowed}")
        return v

    @field_validator('method')
    @classmethod
    def validate_method(cls, v: str) -> str:
        allowed = {"login", "password_reset", "pin_verification", "other"}
        if v not in allowed:
            raise ValueError(f"Method must be one of {allowed}")
        return v


class AuthenticationAttemptResponse(AuthenticationAttemptBase):
    id: str
    user_id: str
    outcome: str
    method: str
    ip_address: str
    timestamp: datetime
