"""
Transaction service for the ATM Withdrawal System.

Provides methods for processing withdrawal transactions, including
balance and limit checks, execution, rollback, and fraud analysis.
All operations are wrapped in atomic database transactions.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Dict, Optional, Tuple

from flask import current_app
from models import db, User, Transaction
from services.audit_service import AuditService
from services.fraud_service import FraudDetectionService


class TransactionService:
    """
    Service handling all withdrawal transaction operations.

    Uses the Flask application's database session (db.session) for all
    database interactions. Ensures atomicity by wrapping operations in
    explicit transactions with commit/rollback.
    """

    @staticmethod
    def process_withdrawal(user: User, amount: Decimal) -> Dict[str, object]:
        """
        Process a withdrawal request for the given user.

        This method performs the following steps:
        1. Validates that the amount is positive and has valid precision.
        2. Checks user balance and daily limit.
        3. Begins a database transaction.
        4. Updates user balance and daily withdrawal counter.
        5. Creates a Transaction record with status 'pending'.
        6. Runs fraud detection analysis.
        7. If suspicious, marks the transaction as flagged.
        8. Sets transaction status to 'approved'.
        9. Logs the success action to audit log.
        10. Commits the transaction.

        If any step fails, the transaction is rolled back and an appropriate
        error response is returned.

        Args:
            user: The User object initiating the withdrawal.
            amount: The amount to withdraw (positive Decimal with ≤2 decimal places).

        Returns:
            A dictionary with keys:
                - 'success': bool indicating whether withdrawal succeeded.
                - 'transaction_id': int (if successful) or None.
                - 'error': str (if failed) or None.
        """
        # 1. Validate amount
        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(str(amount))
            except (ValueError, TypeError):
                return {'success': False, 'transaction_id': None,
                        'error': 'Invalid amount format.'}

        if amount <= 0:
            return {'success': False, 'transaction_id': None,
                    'error': 'Amount must be positive.'}

        if amount.as_tuple().exponent < -2:
            return {'success': False, 'transaction_id': None,
                    'error': 'Amount cannot have more than two decimal places.'}

        # 2. Check balance and daily limit
        check_ok, check_msg = TransactionService.check_balance_and_limit(user, amount)
        if not check_ok:
            # Log declined transaction (no DB commit needed yet; audit log will be flushed)
            AuditService.log_action(
                action='WITHDRAWAL_DECLINED',
                user_id=user.id,
                transaction_id=None,
                details=f"Declined: {check_msg}, amount={amount}"
            )
            try:
                db.session.flush()
            except Exception:
                # Best-effort audit logging; ignore flush errors
                pass
            return {'success': False, 'transaction_id': None, 'error': check_msg}

        # 3. Begin atomic transaction
        transaction = None
        try:
            # 4. Execute withdrawal (update user and create transaction)
            transaction = TransactionService.execute_withdrawal(user, amount)

            # 5. Run fraud detection
            is_flagged = FraudDetectionService.analyze_transaction(user, transaction)

            if not is_flagged:
                # Mark transaction as approved
                transaction.set_status('approved')

            # 6. Log success (still within the same DB transaction)
            AuditService.log_action(
                action='WITHDRAWAL_SUCCESS',
                user_id=user.id,
                transaction_id=transaction.id,
                details=f"Withdrawal of {amount} successful. "
                        f"New balance: {user.balance}"
            )

            # 7. Commit the entire transaction (withdrawal, fraud flag, audit log)
            db.session.commit()

            return {'success': True, 'transaction_id': transaction.id, 'error': None}

        except Exception as exc:
            # Rollback on any failure
            db.session.rollback()
            # Perform additional cleanup if transaction object was created
            if transaction is not None:
                TransactionService.rollback(transaction, exception=exc)
            error_msg = str(exc) if current_app.debug else "Internal error during withdrawal."
            return {'success': False, 'transaction_id': None, 'error': error_msg}

    @staticmethod
    def check_balance_and_limit(user: User, amount: Decimal) -> Tuple[bool, Optional[str]]:
        """
        Verify that the user has sufficient balance and that the withdrawal
        does not exceed the daily limit, taking into account today's
        already withdrawn amount.

        If today is different from user.last_withdrawal_date, the daily
        withdrawn counter is treated as zero for the check (the actual reset
        happens in execute_withdrawal). This method does not modify the database;
        it only performs checks.

        Args:
            user: The User object (expected to have .balance, .daily_limit,
                  .daily_withdrawn_today, .last_withdrawal_date).
            amount: The amount to withdraw.

        Returns:
            A tuple (is_valid: bool, error_message: Optional[str]).
            If valid, error_message is None; otherwise, it describes the reason.
        """
        # Use UTC date to match transaction timestamps
        today = datetime.now(timezone.utc).date()

        # Determine effective daily withdrawn amount for today
        if user.last_withdrawal_date != today:
            effective_daily_withdrawn = Decimal('0.00')
        else:
            effective_daily_withdrawn = user.daily_withdrawn_today

        # Check balance
        if user.balance < amount:
            return (False, 'Insufficient balance.')

        # Check daily limit (including today's withdrawn)
        if effective_daily_withdrawn + amount > user.daily_limit:
            remaining = user.daily_limit - effective_daily_withdrawn
            return (False, f'Exceeds daily limit. Remaining withdrawal capacity: {remaining}.')

        return (True, None)

    @staticmethod
    def execute_withdrawal(user: User, amount: Decimal) -> Transaction:
        """
        Execute a withdrawal by updating the user's balance and daily withdrawal
        counter, and creating a Transaction record.

        Assumes all checks have been passed. This method does NOT commit;
        it flushes changes to the database within the current transaction.

        Args:
            user: The User object.
            amount: The amount to withdraw.

        Returns:
            The created Transaction object (status = 'pending').

        Raises:
            Exception: If any database operation fails.
        """
        # Use UTC date for consistency with timestamps
        today = datetime.now(timezone.utc).date()

        # Reset daily counter if new day
        if user.last_withdrawal_date != today:
            user.daily_withdrawn_today = Decimal('0.00')
            user.last_withdrawal_date = today

        # Update balance and daily withdrawn
        user.balance -= amount
        user.daily_withdrawn_today += amount

        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            amount=amount,
            timestamp=datetime.utcnow(),
            status='pending',
            is_flagged=False
        )
        db.session.add(transaction)

        # Flush to get transaction.id and ensure constraints are checked
        db.session.flush()

        return transaction

    @staticmethod
    def rollback(transaction: Optional[Transaction] = None, exception: Optional[Exception] = None) -> None:
        """
        Perform cleanup after a failed withdrawal.

        This method is called after the database session rollback. It logs
        the failure via the audit service. The audit log entry will be part of
        the next transaction (or will be flushed later). This method does not
        raise any exceptions.

        Args:
            transaction: The Transaction object that was being processed, or None.
            exception: The exception that caused the rollback, if any.
        """
        if transaction is None:
            return

        # Build details string
        details = f"Rollback of withdrawal of {transaction.amount}"
        if exception is not None:
            details += f" due to: {str(exception)}"

        # Log the rollback (safe after rollback; will be part of next transaction)
        try:
            AuditService.log_action(
                action='WITHDRAWAL_ROLLBACK',
                user_id=transaction.user_id,
                transaction_id=transaction.id,
                details=details
            )
            # Flush to ensure the log entry is written promptly
            db.session.flush()
        except Exception:
            # Best-effort logging – ignore failures to avoid masking original error
            pass
