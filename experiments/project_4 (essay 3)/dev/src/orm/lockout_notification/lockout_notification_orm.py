from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class LockoutNotificationORM(Base):
    __tablename__ = "lockout_notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lockout_id: Mapped[int] = mapped_column(Integer, ForeignKey("lockout_record.id"), nullable=False)
    lockout: Mapped["LockoutRecordORM"] = relationship("LockoutRecordORM")
