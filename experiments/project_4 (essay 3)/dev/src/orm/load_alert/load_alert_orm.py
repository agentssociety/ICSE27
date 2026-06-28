from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class LoadAlertORM(Base):
    __tablename__ = "load_alert"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    highLoad: Mapped[bool] = mapped_column(Boolean, nullable=False)
