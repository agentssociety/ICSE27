from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class FriendshipORM(Base):
    __tablename__ = "friendship"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    abstract_isMutual: Mapped[bool] = mapped_column(Boolean, nullable=False)
