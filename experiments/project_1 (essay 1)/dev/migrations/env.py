from __future__ import annotations

import sys
from pathlib import Path

# The Alembic runtime adds the directory containing this file to sys.path,
# which shadows the installed 'alembic' package if the directory is named 'alembic'.
# Remove that directory so that the real alembic package can be imported.
_current_dir = Path(__file__).resolve().parent
if str(_current_dir) in sys.path:
    sys.path.remove(str(_current_dir))

# Add the src directory to sys.path so that 'src' modules can be imported.
# This avoids exposing the local 'alembic' directory as a package via the project root.
sys.path.insert(0, str(_current_dir.parent / 'src'))

from alembic import context
from alembic.config import Config
from sqlalchemy import engine_from_config, pool

from src.config.settings import settings
from src.config.database import Base

# Import all ORM models so Alembic can see them
import src.orm  # noqa: F401 — side-effect: registers all mapped classes

# Create a Config object from the alembic.ini file located in the same directory.
# This replaces `config = context.config` which fails when the environment is
# executed outside the Alembic runtime.
config = Config(str(_current_dir.parent / 'alembic.ini'))
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