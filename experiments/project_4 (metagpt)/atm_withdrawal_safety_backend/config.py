import os
from datetime import timedelta

class Config:
    """Base configuration class for the ATM Withdrawal System."""
    # Secret key for Flask and JWT
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'default-secret-key-change-in-production')
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)

    # Database
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL', 'sqlite:///atm_system.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Bcrypt hashing rounds
    BCRYPT_ROUNDS: int = 12

    # Authentication
    MAX_FAILED_ATTEMPTS: int = 3
    ACCOUNT_LOCK_DURATION_HOURS: int = 24  # Not enforced yet, but configurable

    # Fraud detection thresholds
    FRAUD_THRESHOLDS: dict = {
        'TIME_BETWEEN_WITHDRAWALS_SECONDS': 300,   # 5 minutes
        'DAILY_LIMIT_THRESHOLD_PERCENTAGE': 0.9,   # 90% of daily limit
        'UNUSUAL_HOURS': [0, 1, 2, 3, 4, 5, 23], # Midnight to 5 AM and 11 PM
        'MAX_RAPID_WITHDRAWALS': 3,                # Number of withdrawals within time window
        'RAPID_WITHDRAWAL_WINDOW_SECONDS': 600     # 10 minutes window for rapid check
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL', 'sqlite:///dev_atm_system.db'
    )
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)  # Longer for debugging

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG: bool = False
    # In production, DATABASE_URL must be set to a secure database (e.g., PostgreSQL)
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL', '')
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=30)  # Shorter for security

# Map config names to classes for easy loading
config_mapping = {
    'development': 'DevelopmentConfig',
    'production': 'ProductionConfig',
    'default': 'DevelopmentConfig'
}
