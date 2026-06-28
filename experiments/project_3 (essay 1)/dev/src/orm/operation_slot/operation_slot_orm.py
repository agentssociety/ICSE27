from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class OperationSlotORM(Base):
    __tablename__ = "operation_slot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    op_id: Mapped[int] = mapped_column(Integer, ForeignKey("operation.id"), nullable=False)
    slot_id: Mapped[int] = mapped_column(Integer, ForeignKey("slot.id"), nullable=False)
    op: Mapped["OperationORM"] = relationship("OperationORM")
    slot: Mapped["SlotORM"] = relationship("SlotORM")
