from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class TrafficDataORM(Base):
    __tablename__ = "traffic_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    runwayLoads: Mapped[dict] = mapped_column(JSON, nullable=False)
