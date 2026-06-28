from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class PatientQueueORM(Base):
    __tablename__ = "patient_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    queueId: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
