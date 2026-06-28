from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Numeric, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class WithdrawalTransactionORM(Base):
    __tablename__ = "withdrawal_transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
