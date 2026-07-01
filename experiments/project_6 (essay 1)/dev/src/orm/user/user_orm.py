from __future__ import annotations

from sqlalchemy import Integer, String, Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    passwordHash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    accountStatus: Mapped[str] = mapped_column(String(50), default="pending")
    isAuthenticated: Mapped[bool] = mapped_column(Boolean, default=False)
