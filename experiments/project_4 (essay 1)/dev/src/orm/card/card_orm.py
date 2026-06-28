from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class CardORM(Base):
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    expiryDate: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey("actor.id"), nullable=False)
    owner: Mapped["ActorORM"] = relationship("ActorORM")