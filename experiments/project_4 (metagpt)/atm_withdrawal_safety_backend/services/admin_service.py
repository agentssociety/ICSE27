"""
Admin service for the ATM Withdrawal System.

Provides administrative functions: reviewing flagged transactions,
locking/unlocking accounts, retrieving transaction history, and
accessing audit log history. All operations use database sessions
from the Flask application context.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from flask import current_app
from models import db, User, Transaction, FlaggedTransaction, AuditLog
from services.audit_service import AuditService


class AdminService:
    """
    Service for administrative operations.

    All methods are static and rely on the Flask application's database session.
    """

    @staticmethod
    def review_flagged_transaction(
        flagged_id: int,
        reviewer_id: int,
        status: str
    ) -> None:
        """
        Review a flagged transaction and update its status.

        Args:
            flagged_id: ID of the FlaggedTransaction record.
            reviewer_id: ID of the admin user performing the review.
            status: New review status. Must be 'approved' or 'declined'.

        Raises:
            ValueError: If flagged_id not found or status invalid.
        """
        if status not in ('approved', 'declined'):
            raise ValueError("Status must be 'approved' or 'declined'.")

        flagged: Optional[FlaggedTransaction] = FlaggedTransaction.query.get(flagged_id)
        if flagged is None:
            raise ValueError(f"FlaggedTransaction with id {flagged_id} not found.")

        flagged.reviewed_by = reviewer_id
        flagged.review_status = status
        flagged.review_timestamp = datetime.utcnow()
        db.session.flush()

        # Also update the associated transaction status if needed
        transaction = Transaction.query.get(flagged.transaction_id)
        if transaction:
            if status == 'approved':
                transaction.set_status('approved')
            else:
                transaction.set_status('declined')
            db.session.flush()

        AuditService.log_action(
            action='FLAGGED_REVIEWED',
            user_id=reviewer_id,
            transaction_id=flagged.transaction_id,
            details=f"Flagged transaction {flagged_id} reviewed as {status}."
        )

    @staticmethod
    def lock_unlock_account(user_id: int, lock: bool) -> None:
        """
        Lock or unlock a user account.

        Args:
            user_id: ID of the user whose account status will change.
            lock: True to lock, False to unlock.

        Raises:
            ValueError: If user_id not found.
        """
        user: Optional[User] = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        if lock:
            user.lock_account()
            action_detail = "Account locked by admin."
        else:
            user.unlock_account()
            action_detail = "Account unlocked by admin."
        db.session.flush()

        AuditService.log_action(
            action='ACCOUNT_LOCK_STATUS_CHANGED',
            user_id=user_id,
            transaction_id=None,
            details=action_detail
        )

    @staticmethod
    def get_transaction_history(user_id: int) -> List[Transaction]:
        """
        Retrieve the transaction history for a specific user.

        Args:
            user_id: ID of the user whose transactions to fetch.

        Returns:
            List of Transaction objects ordered by timestamp descending.

        Raises:
            ValueError: If user_id not found.
        """
        user: Optional[User] = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        return Transaction.query.filter_by(user_id=user_id)\
            .order_by(Transaction.timestamp.desc())\
            .all()

    @staticmethod
    def get_audit_logs_history(filters: Optional[dict] = None) -> List[AuditLog]:
        """
        Retrieve audit logs with optional filtering.

        Delegates to AuditService.get_audit_logs for consistency.

        Args:
            filters: A dictionary of filter conditions. Supported keys:
                - 'user_id': int
                - 'action': str
                - 'start_date': datetime (timezone-aware preferred)
                - 'end_date': datetime
                - 'transaction_id': int
                If None, returns all logs.

        Returns:
            List of AuditLog objects ordered by timestamp descending.
        """
        return AuditService.get_audit_logs(filters=filters)
