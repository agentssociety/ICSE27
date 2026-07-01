from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class BiographyORM(Base):
    __tablename__ = "biography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profile.id"), nullable=False)
    profile: Mapped["ProfileORM"] = relationship("ProfileORM")
