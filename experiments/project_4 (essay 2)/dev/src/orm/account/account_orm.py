from __future__ import annotations

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Account domain class

Package: orm.account
Layer: orm
Related tasks: #89, #90, #94
Requirement coverage:
- Account Lock After Three Consecutive Failed PIN Attempts
- Enforce daily transaction limits
- Manual Lock/Unlock User Accounts
"""

class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    daily_limit: Mapped[int] = mapped_column(Integer, default=200)
    used_today: Mapped[int] = mapped_column(Integer, default=0)
    lock_status: Mapped[str] = mapped_column(String(20), default="unlocked")
    failed_attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_failed_count: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[str] = mapped_column(String(36))
