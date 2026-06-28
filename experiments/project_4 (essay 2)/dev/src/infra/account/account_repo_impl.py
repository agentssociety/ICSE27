from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.dto.account.account_dto import AccountData
from src.orm.account.account_orm import AccountORM

"""
Infra layer for the Account domain class

Package: infra.account
Layer: infra
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""


class SQLAlchemyAccountRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, item_id: str) -> Optional[AccountORM]:
        return self._session.get(AccountORM, item_id)

    def update_account(self, account_id: str, data: AccountData) -> None:
        row = self._session.get(AccountORM, account_id)
        if row:
            row.balance = data.balance
            row.daily_limit = data.dailyLimit
            row.used_today = data.usedToday
            self._session.commit()

    def create(self, user_id: str, balance: int = 0, daily_limit: int = 200) -> AccountORM:
        import uuid
        row = AccountORM(
            id=str(uuid.uuid4()),
            user_id=user_id,
            balance=balance,
            daily_limit=daily_limit,
            used_today=0,
            lock_status="unlocked",
            failed_attempt_count=0,
            consecutive_failed_count=0,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row

    def lock_account(self, account_id: str) -> bool:
        row = self._session.get(AccountORM, account_id)
        if row is None:
            return False
        row.lock_status = "locked"
        self._session.commit()
        return True

    def unlock_account(self, account_id: str) -> bool:
        row = self._session.get(AccountORM, account_id)
        if row is None:
            return False
        row.lock_status = "unlocked"
        row.consecutive_failed_count = 0
        self._session.commit()
        return True

    def record_failed_attempt(self, account_id: str) -> bool:
        row = self._session.get(AccountORM, account_id)
        if row is None:
            return False
        row.failed_attempt_count += 1
        row.consecutive_failed_count += 1
        if row.consecutive_failed_count >= 3:
            row.lock_status = "locked"
        self._session.commit()
        return True

    def reset_failed_attempts(self, account_id: str) -> None:
        row = self._session.get(AccountORM, account_id)
        if row:
            row.consecutive_failed_count = 0
            self._session.commit()
