"""
Authentication service for the ATM Withdrawal System.

Provides methods for user authentication, account locking/unlocking,
and retrieving failed login attempts. All operations use SQLAlchemy
sessions from the Flask application context.
"""

from typing import Optional

from flask import current_app
from models import db, User, AuthenticationAttempt
from services.audit_service import AuditService


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed.") -> None:
        self.message = message
        super().__init__(self.message)


class AccountLockedError(AuthenticationError):
    """Exception raised when the account is locked."""

    def __init__(self, message: str = "Account is locked due to too many failed attempts.") -> None:
        self.message = message
        super().__init__(self.message)


class AuthService:
    """
    Service handling user authentication and account status management.
    """

    @staticmethod
    def authenticate(card_number: str, pin: str, ip_address: Optional[str] = None) -> User:
        """
        Authenticate a user by card number and PIN.

        Records all login attempts (successful/failed) into the
        authentication_attempts table and logs every action to the audit log.

        Args:
            card_number: The user's card number (string).
            pin: The plain-text PIN (string).
            ip_address: Optional IP address of the client for audit trail.

        Returns:
            The authenticated User object.

        Raises:
            AuthenticationError: If card number not found or PIN incorrect.
            AccountLockedError: If the account is locked (or becomes locked
                                due to too many failed attempts).
        """
        user: Optional[User] = User.query.filter_by(card_number=card_number).first()

        # Card number not found
        if user is None:
            AuditService.log_action(
                action='LOGIN_FAILED',
                user_id=None,
                transaction_id=None,
                details=f"Invalid card number: {card_number}"
            )
            raise AuthenticationError("Invalid card number or PIN.")

        # Account is already locked
        if user.is_locked:
            AuditService.log_action(
                action='LOGIN_FAILED',
                user_id=user.id,
                transaction_id=None,
                details="Account locked"
            )
            AuthService._record_attempt(user_id=user.id, success=False, ip_address=ip_address)
            raise AccountLockedError("Account is locked. Please contact support.")

        # Verify PIN
        if user.check_pin(pin):
            # Successful authentication
            AuditService.log_action(
                action='LOGIN_SUCCESS',
                user_id=user.id,
                transaction_id=None,
                details="Successful PIN verification"
            )
            AuthService._record_attempt(user_id=user.id, success=True, ip_address=ip_address)
            user.reset_failed_attempts()
            db.session.flush()
            return user
        else:
            # Failed PIN
            user.increment_failed_attempts()
            max_attempts = current_app.config.get('MAX_FAILED_ATTEMPTS', 3)
            attempts = user.failed_attempts
            AuthService._record_attempt(user_id=user.id, success=False, ip_address=ip_address)

            if attempts >= max_attempts:
                # Lock the account
                user.lock_account()
                AuditService.log_action(
                    action='ACCOUNT_LOCKED',
                    user_id=user.id,
                    transaction_id=None,
                    details=f"Account locked after {attempts} failed attempts"
                )
                db.session.flush()
                raise AccountLockedError(
                    "Account has been locked due to too many failed attempts."
                )
            else:
                # Still within allowed attempts
                AuditService.log_action(
                    action='LOGIN_FAILED',
                    user_id=user.id,
                    transaction_id=None,
                    details=f"Invalid PIN (attempt {attempts}/{max_attempts})"
                )
                db.session.flush()
                raise AuthenticationError("Invalid PIN.")

    @staticmethod
    def _record_attempt(user_id: int, success: bool, ip_address: Optional[str] = None) -> None:
        """
        Insert a record into the authentication_attempts table.

        Args:
            user_id: The user ID associated with the attempt.
            success: Whether the attempt was successful.
            ip_address: Optional IP address of the client.
        """
        attempt = AuthenticationAttempt(
            user_id=user_id,
            success=success,
            ip_address=ip_address
        )
        db.session.add(attempt)

    @staticmethod
    def lock_account(user_id: int) -> None:
        """
        Lock a user account by user ID.

        Args:
            user_id: The ID of the user to lock.

        Raises:
            ValueError: If user is not found.
        """
        user: Optional[User] = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        user.lock_account()
        db.session.flush()

    @staticmethod
    def unlock_account(user_id: int) -> None:
        """
        Unlock a user account by user ID and reset failed attempts.

        Args:
            user_id: The ID of the user to unlock.

        Raises:
            ValueError: If user is not found.
        """
        user: Optional[User] = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        user.unlock_account()
        db.session.flush()

    @staticmethod
    def get_failed_attempts(user_id: int) -> int:
        """
        Get the number of consecutive failed login attempts for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The number of failed attempts (int).

        Raises:
            ValueError: If user is not found.
        """
        user: Optional[User] = User.query.get(user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        return user.failed_attempts
