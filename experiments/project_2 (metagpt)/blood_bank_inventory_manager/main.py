"""Main entry point for the Blood Bank Management Application.

This module initializes the Flask application, configures the database,
registers blueprints, sets up the background scheduler, and starts the
development server when executed directly.

The module-level 'app' object is created once and is the intended WSGI
application instance. When run as a script, main() reuses this instance.
"""

import os

from flask import Flask

from config import Config
from app.models import db
from app.routes import main_bp
from app.scheduler import Scheduler


def create_app() -> Flask:
    """Create and configure the Flask application instance.

    Returns:
        Fully configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    # Create all database tables within the application context
    with app.app_context():
        db.create_all()

    # Initialize and start the background scheduler
    _ = Scheduler(app)  # Scheduler starts automatically in its __init__

    return app


def main() -> None:
    """Run the application using the development server.

    This function is intended for development; for production, use WSGI
    server like Gunicorn with the 'app' object exported from this module.
    """
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Use the module-level app instance created once
    application = app
    application.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=debug_mode,
    )


# Expose the application instance for WSGI servers (e.g., Gunicorn)
app = create_app()


if __name__ == "__main__":
    main()
