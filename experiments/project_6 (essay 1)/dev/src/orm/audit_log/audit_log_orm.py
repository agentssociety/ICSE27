from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AuditLogORM(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    adminId: Mapped[str] = mapped_column(String, nullable=False)
    actionType: Mapped[str] = mapped_column(String, nullable=False)
    targetUserId: Mapped[str] = mapped_column(String, nullable=False)
