from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class InterfaceORM(Base):
    __tablename__ = "interface"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[str] = mapped_column(String, nullable=False)
    encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    authenticated: Mapped[bool] = mapped_column(Boolean, nullable=False)
