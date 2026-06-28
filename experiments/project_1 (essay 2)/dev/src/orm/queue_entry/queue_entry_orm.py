from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.config.database import Base


class QueueEntryORM(Base):
    __tablename__ = "queue_entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
