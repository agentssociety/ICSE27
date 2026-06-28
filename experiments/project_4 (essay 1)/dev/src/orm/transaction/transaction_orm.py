from __future__ import annotations

from typing import Optional
import uuid
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class TransactionORM(Base):
    __tablename__ = "transaction"

    transaction_id: Mapped[str] = mapped_column(String, nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[str] = mapped_column(String, nullable=False, default=lambda: str(uuid.uuid4()))
    amount_id: Mapped[int] = mapped_column(Integer, ForeignKey("money.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("state.id"), nullable=False)
    amount: Mapped["MoneyORM"] = relationship("MoneyORM")
    status: Mapped["StateORM"] = relationship("StateORM")