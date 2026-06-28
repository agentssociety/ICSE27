from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class ResourceORM(Base):
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resourceId: Mapped[str] = mapped_column(String, nullable=False)
    resourceType: Mapped[str] = mapped_column(String, nullable=False)
