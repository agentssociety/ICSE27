from __future__ import annotations
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base


class PINORM(Base):
    __tablename__ = "pin"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey("actor.id"), nullable=False)
    owner: Mapped["ActorORM"] = relationship("ActorORM")