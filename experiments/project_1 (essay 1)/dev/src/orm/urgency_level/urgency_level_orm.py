from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class UrgencyLevelORM(Base):
    __tablename__ = "urgency_level"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
