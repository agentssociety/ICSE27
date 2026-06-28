from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import uuid4


class UserRole(str, Enum):
    ADMIN = "admin"
    REGULAR_USER = "regular_user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        username: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.REGULAR_USER,
    ) -> User:
        if not username or not username.strip():
            raise ValueError("Username is required")
        if not email or "@" not in email:
            raise ValueError("Valid email is required")
        if not password_hash:
            raise ValueError("Password hash is required")

        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
            role=role,
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        role: Optional[UserRole] = None,
    ) -> None:
        if username is not None:
            if not username.strip():
                raise ValueError("Username cannot be empty")
            self.username = username.strip()
        if email is not None:
            if "@" not in email:
                raise ValueError("Valid email is required")
            self.email = email.strip().lower()
        if password_hash is not None:
            self.password_hash = password_hash
        if role is not None:
            self.role = role
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.utcnow()

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE
