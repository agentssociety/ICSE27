from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class WithdrawalRecordORM(Base):
    __tablename__ = "withdrawal_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String, nullable=False)
    amount_id: Mapped[int] = mapped_column(Integer, ForeignKey("money.id"), nullable=False)
    amount: Mapped["MoneyORM"] = relationship("MoneyORM")