from __future__ import annotations

from typing import Any, Optional

from src.domain.account import Account, AccountState
from src.infra.account.account_repo_impl import SQLAlchemyAccountRepository


class AuthenticationFlow:
    def __init__(self, repo: SQLAlchemyAccountRepository) -> None:
        self._repo = repo

    def authenticate(self, cardData: str, pinData: str) -> bool:
        accounts = self._repo.get_all()
        if not accounts:
            return False
        account = accounts[0]
        account_obj = Account(failedAttempts=account.failedAttempts)
        result = account_obj.authenticate()
        return result

    def false(self, expired: Any) -> None:
        pass


class AccountManagementService:
    """Service for admin-level account management: lock/unlock accounts."""

    def __init__(self, repo: SQLAlchemyAccountRepository) -> None:
        self._repo = repo

    def lock_account(self, account_id: int, reason: str = "") -> bool:
        """Lock a user account so they cannot log in.

        Args:
            account_id: The database ID of the account to lock.
            reason: Optional reason for locking (e.g., 'suspicious activity').

        Returns:
            True if the account was found and locked, False if not found.
        """
        account_dto = self._repo.get_by_id(account_id)
        if account_dto is None:
            return False

        account = Account(
            failedAttempts=account_dto.failedAttempts,
            balance=account_dto.balance,
            daily_withdrawal_limit=account_dto.daily_withdrawal_limit,
            withdrawn_today=account_dto.withdrawn_today,
        )
        account.lock(reason)

        from src.dto.account.account_dto import AccountUpdate
        update_data = AccountUpdate(
            state=account.state.value,
            locked_reason=account.locked_reason,
        )
        self._repo.update(account_id, update_data)
        return True

    def unlock_account(self, account_id: int) -> bool:
        """Unlock a previously locked user account, restoring login access.

        Args:
            account_id: The database ID of the account to unlock.

        Returns:
            True if the account was found and unlocked, False if not found.
        """
        account_dto = self._repo.get_by_id(account_id)
        if account_dto is None:
            return False

        from src.dto.account.account_dto import AccountUpdate
        update_data = AccountUpdate(
            state=AccountState.ACTIVE.value,
            locked_reason=None,
        )
        self._repo.update(account_id, update_data)
        return True

    def get_account_state(self, account_id: int) -> Optional[str]:
        """Get the current state of an account (e.g., 'active', 'locked').

        Args:
            account_id: The database ID of the account.

        Returns:
            'active' or 'locked' if the account exists, None otherwise.
        """
        account_dto = self._repo.get_by_id(account_id)
        if account_dto is None:
            return None
        return account_dto.state if hasattr(account_dto, 'state') else 'active'