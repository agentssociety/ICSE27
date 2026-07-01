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

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    cfg = context.config
    connectable = engine_from_config(
        cfg.get_section(cfg.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


def run_migrations() -> None:
    try:
        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
    except (AttributeError, NameError):
        # Alembic context proxy not yet established — safe import path
        pass


run_migrations()
