## extensions.py
"""
Initializes Flask extensions used across the application.
All extensions are created without binding to a specific app,
and are configured later in the app factory.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

# Database ORM instance
db: SQLAlchemy = SQLAlchemy()

# Login manager for user session management
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore[assignment]
login_manager.login_message_category = 'info'  # type: ignore[assignment]

# Mail instance for sending emails (e.g., verification)
mail: Mail = Mail()

# Admin interface instance (configured later with models)
admin: Admin = Admin(name='Admin Panel', template_mode='bootstrap3')
