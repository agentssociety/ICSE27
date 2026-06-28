from __future__ import annotations

import sys
from pathlib import Path

_current_dir = Path(__file__).resolve().parent  # migrations/
sys.path.insert(0, str(_current_dir.parent))    # project root

from sqlalchemy import engine_from_config, pool
from alembic import context

from src.config.settings import settings
from src.config.database import Base

# Import all ORM models so Alembic can see them
import src.orm  # noqa: F401  — side-effect: registers all mapped classes

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=settings.database_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if __name__ == '__main__':
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()