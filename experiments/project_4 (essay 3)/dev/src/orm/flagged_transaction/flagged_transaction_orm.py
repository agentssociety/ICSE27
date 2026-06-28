from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class FlaggedTransactionORM(Base):
    __tablename__ = "flagged_transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    withdrawal_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    flagged_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="unreviewed")

    __table_args__ = (
        Index("idx_flagged_transactions_status", "status"),
        Index("idx_flagged_transactions_flagged_at", "flagged_at"),
    )

