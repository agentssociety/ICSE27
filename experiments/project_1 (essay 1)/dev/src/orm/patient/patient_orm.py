from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class PatientORM(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patientId: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    patientQueue_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("patient_queue.id"), nullable=True)
    patientQueue: Mapped[Optional["PatientQueueORM"]] = relationship("PatientQueueORM")
    state: Mapped[str] = mapped_column(String(30), nullable=False, default="pending_triage")
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    urgency_level: Mapped[int] = mapped_column(Integer, nullable=False, default=99)
