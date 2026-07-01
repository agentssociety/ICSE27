from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class DifficultyTagORM(Base):
    __tablename__ = "difficulty_tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey("resource.id"), nullable=False)
    resource: Mapped["ResourceORM"] = relationship("ResourceORM")
