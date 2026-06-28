"""
Entry point for the ATM Withdrawal System Flask application.

This module initializes the Flask app, configures extensions (SQLAlchemy,
Flask-Migrate, Flask-Bcrypt, Flask-JWT-Extended, Flask-RESTful),
registers all API endpoints, and provides the main execution block.
"""

import os
from decimal import Decimal

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

import config as config_module
from config import Config, config_mapping
from models import db, bcrypt
from api.auth_api import AuthLogin, AuthLogout
from api.transaction_api import Withdrawal, TransactionHistory
from api.admin_api import FlaggedList, ReviewFlagged, AccountLock


def create_app(config_name: str = 'default') -> Flask:
    """
    Create and configure the Flask application.

    Loads the appropriate configuration class based on the given name,
    initializes all Flask extensions, and registers RESTful API endpoints.

    Args:
        config_name: Name of the configuration to load.
                     Supported values: 'development', 'production', 'default'.

    Returns:
        A fully configured Flask application instance.
    """
    app = Flask(__name__)

    # ------------------------------------------------------------------
    # Configuration loading using the config_mapping dictionary from config.py
    # This avoids duplicate mappings and manual class name imports.
    # ------------------------------------------------------------------
    class_name = config_mapping.get(config_name, 'DevelopmentConfig')
    config_class = getattr(config_module, class_name, Config)
    app.config.from_object(config_class)

    # ------------------------------------------------------------------
    # Initialize Flask extensions
    # ------------------------------------------------------------------
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)            # Must be kept for JWT to work; assigned to unused variable is optional
    Migrate(app, db)           # Flask-Migrate for database migrations

    # ------------------------------------------------------------------
    # Set up Flask-RESTful API and register endpoints
    # ------------------------------------------------------------------
    api = Api(app)

    # Authentication endpoints
    api.add_resource(AuthLogin, '/auth/login')
    api.add_resource(AuthLogout, '/auth/logout')

    # Transaction endpoints
    api.add_resource(Withdrawal, '/withdraw')
    api.add_resource(TransactionHistory, '/history')

    # Admin endpoints
    api.add_resource(FlaggedList, '/admin/flagged')
    api.add_resource(ReviewFlagged, '/admin/review')
    api.add_resource(AccountLock, '/admin/account/lock')

    # ------------------------------------------------------------------
    # CLI commands for database management (development only)
    # ------------------------------------------------------------------
    @app.cli.command('initdb')
    def initdb_command():
        """Create all database tables based on the models."""
        with app.app_context():
            db.create_all()
        print('Database tables created.')

    @app.cli.command('seed')
    def seed_command():
        """Insert sample data into the database for development/testing."""
        from models import User  # Lazy import to avoid circular dependency
        from utils import hash_pin

        with app.app_context():
            card = '1111222233334444'
            existing_user = User.query.filter_by(card_number=card).first()
            if existing_user:
                print('Sample user already exists.')
                return

            user = User(
                card_number=card,
                pin_hash=hash_pin('1234'),
                account_number='00000001',
                balance=Decimal('5000.00'),
                daily_limit=Decimal('1000.00'),
                daily_withdrawn_today=Decimal('0.00'),
                last_withdrawal_date=None,
                is_locked=False,
                failed_attempts=0
            )
            db.session.add(user)
            db.session.commit()
            print(f'Seeded sample user: card {card}, PIN 1234, balance 5000.')

    return app


if __name__ == '__main__':
    # Determine the environment and create the app
    env_config = os.environ.get('FLASK_ENV', 'development')
    application = create_app(config_name=env_config)

    # Start the development server
    application.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=application.config.get('DEBUG', False)
    )
