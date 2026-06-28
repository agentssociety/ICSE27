from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class FlightORM(Base):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flightNumber: Mapped[str] = mapped_column(String, nullable=False)
    airline: Mapped[str] = mapped_column(String, nullable=False)
    origin: Mapped[str] = mapped_column(String, nullable=False)
    destination: Mapped[str] = mapped_column(String, nullable=False)
    scheduledTime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[str] = mapped_column(String, nullable=False, default='')
