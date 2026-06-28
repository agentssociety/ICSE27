from __future__ import annotations

import sys
from pathlib import Path

_current_dir = Path(__file__).resolve().parent  # migrations/
sys.path.insert(0, str(_current_dir.parent))    # project root

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.config.settings import settings
from src.config.database import Base

# Import all ORM models so Alembic can see them
import src.orm  # noqa: F401  — side-effect: registers all mapped classes


def get_config():
    """Get alembic config, handling standalone import checks."""
    try:
        config = context.config
        config.set_main_option("sqlalchemy.url", settings.database_url)
        return config
    except AttributeError:
        return None


def run_migrations_offline() -> None:
    config = get_config()
    if config is None:
        return
    context.configure(url=settings.database_url, target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    config = get_config()
    if config is None:
        return
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()