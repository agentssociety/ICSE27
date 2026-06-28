from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TransfusionRequestORM(Base):
    __tablename__ = "transfusion_request"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patientName: Mapped[str] = mapped_column(String, nullable=False)
    bloodType: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    urgency: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
