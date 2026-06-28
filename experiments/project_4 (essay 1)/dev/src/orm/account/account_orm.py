from __future__ import annotations

from typing import Optional
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AccountORM(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    failedAttempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    daily_withdrawal_limit: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0)
    withdrawn_today: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    locked_reason: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)