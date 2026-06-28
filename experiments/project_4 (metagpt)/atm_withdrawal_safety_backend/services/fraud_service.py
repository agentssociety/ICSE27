"""
Fraud detection service for the ATM Withdrawal System.

Provides rule-based heuristics to identify suspicious withdrawal activities
including rapid successive withdrawals, amounts near daily limit,
and transactions during unusual hours.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional

from flask import current_app
from models import db, Transaction, FlaggedTransaction, User
from services.audit_service import AuditService


class FraudDetectionService:
    """
    Service responsible for detecting and flagging fraudulent transactions
    based on configurable rule-based heuristics.
    """

    @staticmethod
    def analyze_transaction(user: User, transaction: Transaction) -> bool:
        """
        Analyze a transaction for potential fraud using configured thresholds.

        Checks the following rules (all thresholds from app config):
        - Rapid successive withdrawals: time since the last approved withdrawal
          is less than TIME_BETWEEN_WITHDRAWALS_SECONDS.
        - Withdrawal amount close to the daily limit (DAILY_LIMIT_THRESHOLD_PERCENTAGE).
        - Transaction during unusual hours (UNUSUAL_HOURS list).

        If any rule is triggered, the transaction is flagged with an appropriate
        severity and a record is created in the flagged_transactions table.

        Args:
            user: The User object making the withdrawal.
            transaction: The Transaction object to analyze.

        Returns:
            True if the transaction is flagged as suspicious, False otherwise.
        """
        thresholds = current_app.config.get('FRAUD_THRESHOLDS', {})
        now = datetime.utcnow()

        reasons: List[str] = []
        has_rapid = False
        near_limit = False
        unusual_hour = False

        # 1. Rapid successive withdrawals: check time since last approved withdrawal
        rapid_window = thresholds.get('TIME_BETWEEN_WITHDRAWALS_SECONDS', 300)
        last_withdrawal = Transaction.query.filter(
            Transaction.user_id == user.id,
            Transaction.status == 'approved'
        ).order_by(Transaction.timestamp.desc()).first()
        if last_withdrawal:
            time_since_last = (now - last_withdrawal.timestamp).total_seconds()
            if time_since_last < rapid_window:
                has_rapid = True
                reasons.append(
                    f"Time since last withdrawal: {time_since_last:.1f}s < {rapid_window}s"
                )

        # 2. Amount near daily limit
        daily_limit_pct = thresholds.get('DAILY_LIMIT_THRESHOLD_PERCENTAGE', 0.9)
        if transaction.amount >= user.daily_limit * daily_limit_pct:
            near_limit = True
            reasons.append(
                f"Amount {transaction.amount} exceeds {daily_limit_pct:.0%} of "
                f"daily limit ({user.daily_limit})"
            )

        # 3. Unusual hour
        unusual_hours = thresholds.get('UNUSUAL_HOURS', [0, 1, 2, 3, 4, 5, 23])
        if transaction.timestamp.hour in unusual_hours:
            unusual_hour = True
            reasons.append(
                f"Transaction during unusual hour: {transaction.timestamp.hour}"
            )

        if not reasons:
            return False

        # Determine severity using boolean flags
        if len(reasons) >= 3:
            severity = 'high'
        elif len(reasons) >= 2:
            severity = 'high' if has_rapid else 'medium'
        elif has_rapid:
            severity = 'high'
        else:
            severity = 'low'

        combined_reason = '; '.join(reasons)
        FraudDetectionService.flag_transaction(transaction, combined_reason, severity)
        return True

    @staticmethod
    def flag_transaction(
        transaction: Transaction,
        reason: str,
        severity: str = 'low'
    ) -> None:
        """
        Flag a transaction as suspicious and create a FlaggedTransaction record.

        Also updates the transaction's status to 'flagged' and records the
        action in the audit log.

        Args:
            transaction: The Transaction object to flag.
            reason: A human-readable description of why it was flagged.
            severity: Severity level ('low', 'medium', 'high').
        """
        transaction.flag()
        db.session.flush()

        flagged = FlaggedTransaction(
            transaction_id=transaction.id,
            reason=reason,
            severity=severity,
            review_status='pending'
        )
        db.session.add(flagged)
        db.session.flush()

        AuditService.log_action(
            action='TRANSACTION_FLAGGED',
            user_id=transaction.user_id,
            transaction_id=transaction.id,
            details=f"Severity: {severity}, Reason: {reason}"
        )

    @staticmethod
    def get_flagged_transactions(
        review_status: Optional[str] = None
    ) -> List[FlaggedTransaction]:
        """
        Retrieve all flagged transactions, optionally filtered by review status.

        Args:
            review_status: If provided, filter by this status (e.g., 'pending',
                           'approved', 'declined'). If None, return all.

        Returns:
            A list of FlaggedTransaction objects, ordered by transaction timestamp
            descending (most recent first).
        """
        query = FlaggedTransaction.query
        if review_status:
            query = query.filter(FlaggedTransaction.review_status == review_status)
        query = query.join(Transaction).order_by(Transaction.timestamp.desc())
        return query.all()
