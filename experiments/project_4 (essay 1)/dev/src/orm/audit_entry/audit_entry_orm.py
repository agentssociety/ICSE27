from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AuditEntryORM(Base):
    __tablename__ = "audit_entry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    operation_id: Mapped[int] = mapped_column(Integer, ForeignKey("req_fraud_01.id"), nullable=False)
    recordedBy_id: Mapped[str] = mapped_column(String, ForeignKey("actor.id"), nullable=False)
    operation: Mapped["REQ_FRAUD_01ORM"] = relationship("REQ_FRAUD_01ORM")
    recordedBy: Mapped["ActorORM"] = relationship("ActorORM")