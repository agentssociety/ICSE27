from __future__ import annotations

from typing import Any, Optional, Protocol

"""
Repository layer for the Account domain class

Package: repository.account
Layer: repository
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""

from src.dto.account.account_dto import AccountData


class Interface(Protocol):
    def authenticateChannel(self, channelId: str) -> bool:
        ...


class Account_Database(Protocol):
    def get_account(self, account_id: str) -> Optional[AccountData]: ...
    def update_account(self, account_id: str, data: AccountData) -> None: ...


class Payment_Processing_System(Protocol):
    def process_payment(self, account_id: str, amount: int) -> bool: ...


class LockUnlockAPI(Protocol):
    def lock_account(self, account_id: str) -> bool: ...
    def unlock_account(self, account_id: str) -> bool: ...


class UserManagementDatabase(Protocol):
    def get_user(self, user_id: str) -> Any: ...
    def update_user_status(self, user_id: str, status: str) -> None: ...


class UserManagementPage(Protocol):
    def display_locked_users(self) -> list[Any]: ...
    def display_active_users(self) -> list[Any]: ...
