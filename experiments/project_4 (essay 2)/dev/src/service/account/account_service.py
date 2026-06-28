from __future__ import annotations

from typing import Any, Optional, Protocol, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from src.domain.account import Account, AccountStatus, Actor, Admin, Permission, SecurityTeam, State, UserAccount
    from src.domain.transaction import Transaction
    from src.repository.account import Interface

"""
Service layer for the Account domain class

Package: service.account
Layer: service
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""

from src.dto.account.account_dto import AccountData, LoginRequestDTO, LoginResponseDTO, LockStatus


@dataclass
class Operation:
    operationId: str | None = None
    preCondition: State | None = None
    postCondition: State | None = None
    initiator: Actor | None = None
    target: Account | None = None
    transaction: Transaction | None = None
    interfaces: list[Interface] | None = None
    permission: Permission | None = None
    preState: State | None = None
    postState: State | None = None

    def createOperation(self, state: State.Pre2, result: State.Post2) -> None:
        pass


class LockUnlockService(Protocol):
    def lockAccount(self, admin: Admin, account: UserAccount) -> None:
        ...

    def unlockAccount(self, admin: Admin, account: UserAccount) -> None:
        ...

    def getAccountStatus(self, team: SecurityTeam, account: UserAccount) -> AccountStatus:
        ...


class AuthorizationService:
    """Handles transaction authorization with balance and daily limit checks."""

    def __init__(self, repository: Any) -> None:
        self._repository = repository

    def authorize_transaction(self, account_id: str, amount: int) -> tuple[bool, str]:
        """Check if a transaction is authorized.

        Returns (authorized: bool, reason: str).
        """
        account_orm = self._repository.get_by_id(account_id)
        if account_orm is None:
            return False, "Account not found"

        if account_orm.lock_status == "locked":
            return False, "Account is locked"

        if account_orm.balance < amount:
            return False, "Insufficient funds"

        if account_orm.used_today + amount > account_orm.daily_limit:
            return False, "Daily limit exceeded"

        return True, "Authorized"


class LoginService:
    """Handles login with PIN verification and account lock logic."""

    def __init__(self, account_repository: Any, pin_repository: Any) -> None:
        self._account_repo = account_repository
        self._pin_repo = pin_repository

    def handle_login(self, user_id: str, pin: str) -> LoginResponseDTO:
        # Look up account for user
        account_orm = self._account_repo.get_by_id(user_id)
        if account_orm is None:
            return LoginResponseDTO(success=False, lockStatus=LockStatus.UNLOCKED, message="Account not found")

        if account_orm.lock_status == "locked":
            return LoginResponseDTO(success=False, lockStatus=LockStatus.LOCKED, message="Account is locked")

        # Verify PIN (simplified - look up pin in pin repo)
        pin_orm = self._pin_repo.get_by_id(user_id) if hasattr(self._pin_repo, 'get_by_id') else None
        pin_valid = pin_orm is not None and hasattr(pin_orm, 'pin_code') and pin_orm.pin_code == pin

        if pin_valid:
            self._account_repo.reset_failed_attempts(user_id)
            return LoginResponseDTO(success=True, lockStatus=LockStatus.UNLOCKED, message="Login successful")
        else:
            self._account_repo.record_failed_attempt(user_id)
            account_orm = self._account_repo.get_by_id(user_id)
            is_locked = account_orm is not None and account_orm.lock_status == "locked"
            new_status = LockStatus.LOCKED if is_locked else LockStatus.UNLOCKED
            return LoginResponseDTO(
                success=False,
                lockStatus=new_status,
                message="Invalid PIN" if not is_locked else "Account locked due to multiple failed attempts"
            )
