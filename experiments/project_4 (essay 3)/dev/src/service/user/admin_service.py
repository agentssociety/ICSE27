from __future__ import annotations

from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session

from src.infra.withdrawal_transaction.withdrawal_transaction_repo_impl import SQLAlchemyWithdrawalTransactionRepository
from src.infra.flagged_transaction.flagged_transaction_repo_impl import SQLAlchemyFlaggedTransactionRepository
from src.infra.user.user_repo_impl import SQLAlchemyUserRepository
from src.dto.withdrawal_transaction.withdrawal_transaction_dto import WithdrawalResponse, WithdrawalListResponse
from src.dto.flagged_transaction.flagged_transaction_dto import FlaggedTransactionResponse, FlaggedTransactionListResponse
from src.dto.user.user_dto import UserResponse
from src.domain.user.User import User, UserRole, UserStatus


class AdminService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._withdrawal_repo = SQLAlchemyWithdrawalTransactionRepository(session)
        self._flagged_repo = SQLAlchemyFlaggedTransactionRepository(session)
        self._user_repo = SQLAlchemyUserRepository(session)

    def _verify_admin(self, user_id: str) -> None:
        user = self._user_repo.get_by_id(user_id)
        if user is None:
            raise PermissionError("User not found")
        if user.role != UserRole.ADMIN.value:
            raise PermissionError("User is not an admin")
        if user.status != UserStatus.ACTIVE.value:
            raise PermissionError("Admin user is not active")

    def list_all_withdrawals(
        self,
        admin_user_id: str,
        status_filter: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        account_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> WithdrawalListResponse:
        self._verify_admin(admin_user_id)
        # Get all withdrawal transactions
        items = self._withdrawal_repo.get_all(skip=skip, limit=limit)
        
        # Apply filters
        if status_filter:
            items = [i for i in items if i.status == status_filter]
        if date_from:
            items = [i for i in items if i.timestamp >= date_from]
        if date_to:
            items = [i for i in items if i.timestamp <= date_to]
        if amount_min is not None:
            items = [i for i in items if float(i.amount) >= amount_min]
        if amount_max is not None:
            items = [i for i in items if float(i.amount) <= amount_max]
        if account_id:
            items = [i for i in items if i.account_id == account_id]
        
        total = len(items)
        paginated = items[skip:skip + limit]
        return WithdrawalListResponse(items=paginated, total=total)

    def list_all_flagged_transactions(
        self,
        admin_user_id: str,
        status_filter: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        account_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> FlaggedTransactionListResponse:
        self._verify_admin(admin_user_id)
        items = self._flagged_repo.get_all(status_filter=status_filter, skip=skip, limit=limit)
        
        # Apply additional filters
        if date_from:
            items = [i for i in items if i.flagged_at >= date_from]
        if date_to:
            items = [i for i in items if i.flagged_at <= date_to]
        
        total = len(items)
        paginated = items[skip:skip + limit]
        return FlaggedTransactionListResponse(items=paginated, total=total)

    def get_withdrawal_detail(
        self, admin_user_id: str, withdrawal_id: str
    ) -> Optional[WithdrawalResponse]:
        self._verify_admin(admin_user_id)
        return self._withdrawal_repo.get_by_id(withdrawal_id)

    def get_flagged_detail(
        self, admin_user_id: str, flagged_id: str
    ) -> Optional[FlaggedTransactionResponse]:
        self._verify_admin(admin_user_id)
        return self._flagged_repo.get_by_id(flagged_id)

    def review_flagged_transaction(
        self, admin_user_id: str, flagged_id: str
    ) -> Optional[FlaggedTransactionResponse]:
        self._verify_admin(admin_user_id)
        return self._flagged_repo.update_review(flagged_id, admin_user_id)
