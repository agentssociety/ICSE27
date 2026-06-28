"""ORM models for the ATM Withdrawal System."""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Database instance to be initialized with Flask app
db: SQLAlchemy = SQLAlchemy()
# Bcrypt instance for password hashing
bcrypt: Bcrypt = Bcrypt()


class User(db.Model):
    """Represents a bank account user."""
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_number: str = db.Column(db.String(20), unique=True, nullable=False, index=True)
    pin_hash: str = db.Column(db.String(128), nullable=False)
    account_number: str = db.Column(db.String(20), unique=True, nullable=False)
    balance: Decimal = db.Column(db.Numeric(12, 2), default=Decimal('0.00'), nullable=False)
    daily_limit: Decimal = db.Column(db.Numeric(12, 2), default=Decimal('1000.00'), nullable=False)
    daily_withdrawn_today: Decimal = db.Column(db.Numeric(12, 2), default=Decimal('0.00'), nullable=False)
    last_withdrawal_date: Optional[date] = db.Column(db.Date, nullable=True)
    is_locked: bool = db.Column(db.Boolean, default=False, nullable=False)
    failed_attempts: int = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    authentication_attempts = db.relationship('AuthenticationAttempt', backref='user', lazy='dynamic')

    def check_pin(self, pin: str) -> bool:
        """Verify the provided PIN against the stored hash."""
        return bcrypt.check_password_hash(self.pin_hash, pin)

    def increment_failed_attempts(self) -> None:
        """Increase failed login attempts and lock account if threshold exceeded."""
        self.failed_attempts += 1
        db.session.flush()  # Ensure updated value is visible

    def reset_failed_attempts(self) -> None:
        """Reset failed login attempts to zero."""
        self.failed_attempts = 0

    def lock_account(self) -> None:
        """Lock the user account."""
        self.is_locked = True

    def unlock_account(self) -> None:
        """Unlock the user account."""
        self.is_locked = False
        self.failed_attempts = 0


class Transaction(db.Model):
    """Represents a single withdrawal transaction."""
    __tablename__ = 'transactions'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount: Decimal = db.Column(db.Numeric(12, 2), nullable=False)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status: str = db.Column(
        db.String(20),
        default='pending',
        # pending, approved, declined, flagged
        nullable=False
    )
    decline_reason: Optional[str] = db.Column(db.Text, nullable=True)
    is_flagged: bool = db.Column(db.Boolean, default=False, nullable=False)

    # Relationship to FlaggedTransaction
    flagged_transaction = db.relationship('FlaggedTransaction', uselist=False, backref='transaction')

    def set_status(self, status: str) -> None:
        """Update the transaction status."""
        valid_statuses = {'pending', 'approved', 'declined', 'flagged'}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
        self.status = status

    def flag(self) -> None:
        """Mark this transaction as flagged."""
        self.is_flagged = True
        self.status = 'flagged'


class AuthenticationAttempt(db.Model):
    """Records each login attempt for auditing."""
    __tablename__ = 'authentication_attempts'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    success: bool = db.Column(db.Boolean, nullable=False)
    ip_address: Optional[str] = db.Column(db.String(45), nullable=True)  # IPv4/IPv6


class AuditLog(db.Model):
    """Central audit log for all system actions."""
    __tablename__ = 'audit_logs'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action: str = db.Column(db.String(100), nullable=False)
    user_id: Optional[int] = db.Column(db.Integer, nullable=True)  # May be None for system actions
    transaction_id: Optional[int] = db.Column(db.Integer, nullable=True)
    details: Optional[str] = db.Column(db.Text, nullable=True)
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)


class FlaggedTransaction(db.Model):
    """Stores details about flagged suspicious transactions."""
    __tablename__ = 'flagged_transactions'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id: int = db.Column(db.Integer, db.ForeignKey('transactions.id'), unique=True, nullable=False)
    reason: str = db.Column(db.String(255), nullable=False)
    severity: str = db.Column(
        db.String(20),
        default='low',
        # low, medium, high
        nullable=False
    )
    reviewed_by: Optional[int] = db.Column(db.Integer, nullable=True)  # Admin user ID
    review_status: Optional[str] = db.Column(
        db.String(20),
        nullable=True
        # e.g., pending, approved, declined
    )
    review_timestamp: Optional[datetime] = db.Column(db.DateTime, nullable=True)
