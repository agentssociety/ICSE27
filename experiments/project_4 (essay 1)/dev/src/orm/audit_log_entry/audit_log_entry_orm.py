from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AuditLogEntryORM(Base):
    __tablename__ = "audit_log_entry"

    operation: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    ip_address: Mapped[str] = mapped_column(String, nullable=False)
    outcome: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, primary_key=True, default=None)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
    action_type: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)