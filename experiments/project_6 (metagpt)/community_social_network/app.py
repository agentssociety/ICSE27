#!/usr/bin/env python3
"""
Main application entry point for the Social Media Platform.
Creates Flask app, initializes extensions, registers blueprints, and runs the server.
"""

import os
from typing import Any

from flask import Flask, render_template
from flask_migrate import Migrate

from config import Config
from extensions import db, login_manager, mail, admin
from routes_auth import auth_bp
from routes_main import main_bp
from routes_admin import admin_bp
from routes_api import api_bp


def create_app(config_class: Any = Config) -> Flask:
    """
    Application factory function.

    Args:
        config_class: Configuration class (default: Config).

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    # Optionally, add Flask-Migrate for database migrations
    # migrate = Migrate(app, db)  # Uncomment if needed

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Create database tables if they don't exist (for development convenience)
    with app.app_context():
        db.create_all()

    # Error handlers
    @app.errorhandler(404)
    def not_found(error: Any) -> tuple:
        """Handle 404 errors with a custom template."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(error: Any) -> tuple:
        """Handle 403 errors with a custom template."""
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error: Any) -> tuple:
        """Handle 500 errors with a custom template and rollback session."""
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Ensure the upload folder exists
    upload_folder: str = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_folder, exist_ok=True)

    # Exempt static files from CSRF if needed (Flask-WTF handles it)
    # This is typically not required; forms already have CSRF.

    return app


if __name__ == '__main__':
    # Create the application instance and run it
    application = create_app()
    application.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    )
