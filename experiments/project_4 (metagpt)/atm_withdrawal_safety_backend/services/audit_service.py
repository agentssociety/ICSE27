"""
Audit service for the ATM Withdrawal System.

Provides methods for recording and retrieving audit log entries.
All operations use SQLAlchemy sessions from the Flask application context.
"""

from typing import List, Optional
from datetime import datetime

from models import db, AuditLog


class AuditService:
    """
    Service handling audit logging and retrieval.
    """

    @staticmethod
    def log_action(
        action: str,
        user_id: Optional[int] = None,
        transaction_id: Optional[int] = None,
        details: Optional[str] = None
    ) -> None:
        """
        Record an action in the audit log.

        Args:
            action: A string describing the action (e.g., 'LOGIN_SUCCESS', 'WITHDRAWAL_SUCCESS').
            user_id: The ID of the user involved (can be None for system actions).
            transaction_id: The ID of the related transaction (optional).
            details: Additional details or reasons for the action (optional).
        """
        log_entry = AuditLog(
            action=action,
            user_id=user_id,
            transaction_id=transaction_id,
            details=details,
            timestamp=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.flush()  # Ensure the entry is written without committing the whole transaction

    @staticmethod
    def get_audit_logs(filters: Optional[dict] = None) -> List[AuditLog]:
        """
        Retrieve audit logs with optional filtering.

        Args:
            filters: A dictionary of filter conditions. Supported keys:
                - 'user_id': int, filter by user ID.
                - 'action': str, filter by action name.
                - 'start_date': datetime, filter logs after this datetime.
                - 'end_date': datetime, filter logs before this datetime.
                - 'transaction_id': int, filter by transaction ID.
                If None, returns all logs.

        Returns:
            A list of AuditLog objects matching the filters. Ordered by timestamp descending.
        """
        query = AuditLog.query

        if filters:
            # Filter by user_id
            if 'user_id' in filters and filters['user_id'] is not None:
                query = query.filter(AuditLog.user_id == filters['user_id'])

            # Filter by action
            if 'action' in filters and filters['action'] is not None:
                query = query.filter(AuditLog.action == filters['action'])

            # Filter by datetime range
            if 'start_date' in filters and filters['start_date'] is not None:
                query = query.filter(AuditLog.timestamp >= filters['start_date'])

            if 'end_date' in filters and filters['end_date'] is not None:
                query = query.filter(AuditLog.timestamp <= filters['end_date'])

            # Filter by transaction_id
            if 'transaction_id' in filters and filters['transaction_id'] is not None:
                query = query.filter(AuditLog.transaction_id == filters['transaction_id'])

        # Order by most recent first
        query = query.order_by(AuditLog.timestamp.desc())

        return query.all()
