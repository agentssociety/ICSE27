from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class FlightORM(Base):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    flightNumber: Mapped[str] = mapped_column(String, nullable=False)
    aircraftType: Mapped[str] = mapped_column(String, nullable=False)
