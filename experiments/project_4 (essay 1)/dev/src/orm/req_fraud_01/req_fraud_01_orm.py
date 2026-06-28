from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class REQ_FRAUD_01ORM(Base):
    __tablename__ = "req_fraud_01"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    initiator_id: Mapped[str] = mapped_column(String, ForeignKey("actor.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, ForeignKey("resource.id"), nullable=False)
    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("interface.id"), nullable=False)
    pre_id: Mapped[int] = mapped_column(Integer, ForeignKey("state.id"), nullable=False)
    initiator: Mapped["ActorORM"] = relationship("ActorORM")
    target: Mapped["ResourceORM"] = relationship("ResourceORM")
    channel: Mapped["InterfaceORM"] = relationship("InterfaceORM")
    pre: Mapped["StateORM"] = relationship("StateORM")