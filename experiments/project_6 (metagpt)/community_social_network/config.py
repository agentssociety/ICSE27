## config.py
import os

class Config:
    """Application configuration class with default values for all settings."""
    # Secret key for session signing and CSRF protection
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'hard-to-guess-secret-key')

    # Database configuration
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL', 'sqlite:///site.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Mail server configuration (Flask-Mail)
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT: int = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS: bool = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER: str = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')

    # Upload configuration (Pillow processed images)
    UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB

    # Flask-Admin and additional settings
    FLASK_ADMIN_SWATCH: str = 'cerulean'
