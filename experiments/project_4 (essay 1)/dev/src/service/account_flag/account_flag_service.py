
from __future__ import annotations

from typing import Any, Optional, Protocol
from datetime import datetime, timedelta
from statistics import mean

from src.domain.account_flag import AccountFlag, FlagReason
from src.infra.account_flag.account_flag_repo_impl import SQLAlchemyAccountFlagRepository
from src.infra.transaction.transaction_repo_impl import SQLAlchemyTransactionRepository
from src.dto.account_flag.account_flag_dto import AccountFlagCreate, AccountFlagUpdate, AccountFlagResponse


class AccountFlagService(Protocol):
    def detect_and_flag(self, account_id: int, transaction_id: str, amount: float, timestamp: str) -> Optional[AccountFlagResponse]:
        """Check if a withdrawal should be flagged and create a flag if needed."""
        ...
    def get_flags_for_account(self, account_id: int) -> list[AccountFlagResponse]:
        """Get all flags for a specific account."""
        ...
    def get_all_flags(self) -> list[AccountFlagResponse]:
        """Get all account flags."""
        ...


class AccountFlagServiceImpl:
    """Service that monitors withdrawal transactions and flags unusual patterns.

    Detection rules:
    1. Rapid consecutive withdrawals: more than 3 withdrawals within 5 minutes
    2. Unusual amount: withdrawal amount > 10x the historical average
    """

    RAPID_WITHDRAWAL_WINDOW_MINUTES = 5
    RAPID_WITHDRAWAL_THRESHOLD = 3
    UNUSAL_AMOUNT_MULTIPLIER = 10

    def __init__(
        self,
        account_flag_repo: SQLAlchemyAccountFlagRepository,
        transaction_repo: SQLAlchemyTransactionRepository,
    ) -> None:
        self._flag_repo = account_flag_repo
        self._txn_repo = transaction_repo

    def detect_rapid_consecutive_withdrawals(self, account_id: int, timestamp: str) -> bool:
        """Check if there have been more than threshold withdrawals within the time window."""
        try:
            current_time = datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            # If timestamp parsing fails, use current time
            current_time = datetime.now()

        window_start = current_time - timedelta(minutes=self.RAPID_WITHDRAWAL_WINDOW_MINUTES)
        window_start_str = window_start.isoformat()

        # Fetch recent transactions for this account (within the time window)
        recent_txns = self._txn_repo.get_by_user_id(account_id)

        # Count transactions within the window (excluding the current one if already recorded)
        count = 0
        for txn in recent_txns:
            try:
                txn_time = datetime.fromisoformat(txn.timestamp)
                if txn_time >= window_start and txn_time <= current_time:
                    count += 1
            except (ValueError, TypeError):
                pass

        return count > self.RAPID_WITHDRAWAL_THRESHOLD

    def detect_unusual_amount(self, account_id: int, amount: float) -> bool:
        """Check if the withdrawal amount is significantly above the historical average."""
        recent_txns = self._txn_repo.get_by_user_id(account_id)

        if not recent_txns:
            # No history - not unusual
            return False

        amounts = []
        for txn in recent_txns:
            try:
                amounts.append(float(txn.amount))
            except (ValueError, TypeError, AttributeError):
                pass

        if not amounts:
            return False

        avg_amount = mean(amounts)
        if avg_amount <= 0:
            return False

        return amount > (avg_amount * self.UNUSAL_AMOUNT_MULTIPLIER)

    def detect_and_flag(self, account_id: int, transaction_id: str, amount: float, timestamp: str) -> Optional[AccountFlagResponse]:
        """Check if a withdrawal should be flagged and create a flag if needed.

        Returns the created flag if detected, None otherwise.
        """
        reason = None

        if self.detect_rapid_consecutive_withdrawals(account_id, timestamp):
            reason = FlagReason.RAPID_CONSECUTIVE_WITHDRAWALS
        elif self.detect_unusual_amount(account_id, amount):
            reason = FlagReason.UNUSUAL_AMOUNT

        if reason is None:
            return None

        flag_create = AccountFlagCreate(
            account_id=account_id,
            transaction_id=transaction_id,
        )
        return self._flag_repo.create(flag_create)

    def get_flags_for_account(self, account_id: int) -> list[AccountFlagResponse]:
        """Get all flags for a specific account."""
        all_flags = self._flag_repo.get_all()
        return [f for f in all_flags if f.account_id == account_id]

    def get_all_flags(self) -> list[AccountFlagResponse]:
        """Get all account flags."""
        return self._flag_repo.get_all()
