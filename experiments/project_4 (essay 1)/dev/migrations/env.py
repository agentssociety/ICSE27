from __future__ import annotations

import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.config.settings import settings
from src.config.database import Base

# Import all ORM models so Alembic can see them
try:
    import src.orm  # noqa: F401  — side-effect: registers all mapped classes
except ImportError:
    # If the ORM module is not fully set up (e.g., missing base), skip registration.
    pass

# When imported directly (not via alembic CLI), context.config is not available
config = getattr(context, 'config', None)
if config is not None:
    config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=settings.database_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Only attempt to determine offline/online mode when the context proxy is available
if config is not None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()