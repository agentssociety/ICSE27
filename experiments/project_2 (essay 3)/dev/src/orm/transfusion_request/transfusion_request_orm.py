from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class TransfusionRequestORM(Base):
    __tablename__ = "transfusion_request"

    requestId: Mapped[str] = mapped_column(String, nullable=False)
    patientId: Mapped[str] = mapped_column(String, nullable=False)
    patientABORh: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    bloodType: Mapped[str] = mapped_column(String, nullable=False)
    patientID: Mapped[str] = mapped_column(String, nullable=False)
