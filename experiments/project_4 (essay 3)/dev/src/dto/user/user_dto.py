from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(UserBase):
    username: str
    email: str
    password_hash: str
    role: str = "regular_user"

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v.strip().lower()

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username is required")
        return v.strip()

    @field_validator('password_hash')
    @classmethod
    def validate_password_hash(cls, v: str) -> str:
        if not v:
            raise ValueError("Password hash is required")
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed = {"admin", "regular_user"}
        if v not in allowed:
            raise ValueError(f"Role must be one of {allowed}")
        return v


class UserUpdateRequest(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email_opt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and "@" not in v:
            raise ValueError("Email must contain @")
        return v.strip().lower() if v else v

    @field_validator('username')
    @classmethod
    def validate_username_opt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Username cannot be empty")
        return v.strip() if v else v

    @field_validator('role')
    @classmethod
    def validate_role_opt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed = {"admin", "regular_user"}
            if v not in allowed:
                raise ValueError(f"Role must be one of {allowed}")
        return v


class UserResponse(UserBase):
    id: str
    username: str
    email: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime


class UserListResponse(UserBase):
    items: list[UserResponse]
    total: int
