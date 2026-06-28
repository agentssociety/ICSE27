from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class DailyWithdrawalLimitORM(Base):
    __tablename__ = "daily_withdrawal_limits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    daily_limit: Mapped[float] = mapped_column(Float, nullable=False, default=200.0)
    used_today: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reset_time: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

