from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    email: str
    password: str
    name: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    email: str
    name: str
    accountStatus: str
    isAuthenticated: bool


class RegistrationRequest(BaseModel):
    email: str
    password: str
    name: str


class RegistrationResponse(BaseModel):
    userId: int
    email: str
    message: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    userId: int
    email: str
    name: str
    message: str


class SoftDeleteRequest(BaseModel):
    pass


class RecoveryRequest(BaseModel):
    pass


class AccountStatusResponse(BaseModel):
    status: str

