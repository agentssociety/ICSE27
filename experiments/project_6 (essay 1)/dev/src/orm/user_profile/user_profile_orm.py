from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class UserProfileORM(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    verifiedBadgeStatus: Mapped[bool] = mapped_column(Boolean, nullable=False)
