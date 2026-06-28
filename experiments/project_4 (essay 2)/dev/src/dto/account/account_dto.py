from __future__ import annotations


from pydantic import BaseModel, ConfigDict
from enum import Enum

"""
Dto layer for the Account domain class

Package: dto.account
Layer: dto
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""


class LockStatus(str, Enum):
    UNLOCKED = "unlocked"
    LOCKED = "locked"


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class LoginRequestDTO(BaseModel):
    userId: str
    pin: str


class LoginResponseDTO(BaseModel):
    success: bool
    lockStatus: LockStatus
    message: str


class UnlockRequestDTO(BaseModel):
    userId: str
    adminId: str


class UnlockResponseDTO(BaseModel):
    success: bool
    message: str


class AuthorizationRequest(BaseModel):
    initiatorId: str
    accountId: str
    amount: int
    permission: Permission
    interfaceType: str


class AuthorizationResponse(BaseModel):
    authorized: bool
    newBalance: int
    newUsedToday: int
    reason: str


class AccountData(BaseModel):
    balance: int
    dailyLimit: int
    usedToday: int

    def validateAccountData(self, balance: int, dailyLimit: int, usedToday: int) -> bool:
        return balance >= 0 and dailyLimit >= 0 and usedToday >= 0
