from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class AuthenticationMethod(str, Enum):
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"
    PIN_VERIFICATION = "pin_verification"
    OTHER = "other"


class AuthenticationOutcome(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class AuthenticationAttempt:
    id: str
    user_id: str
    outcome: AuthenticationOutcome
    method: AuthenticationMethod
    ip_address: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        user_id: str,
        outcome: AuthenticationOutcome,
        method: AuthenticationMethod = AuthenticationMethod.LOGIN,
        ip_address: str = "0.0.0.0",
    ) -> AuthenticationAttempt:
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            outcome=outcome,
            method=method,
            ip_address=ip_address,
            timestamp=datetime.utcnow(),
        )
