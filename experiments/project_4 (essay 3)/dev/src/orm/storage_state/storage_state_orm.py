from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class StorageStateORM(Base):
    __tablename__ = "storage_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    used: Mapped[int] = mapped_column(Integer, nullable=False)
