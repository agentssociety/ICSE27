from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class StudentAccountORM(Base):
    __tablename__ = "student_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    registrationData_id: Mapped[int] = mapped_column(Integer, ForeignKey("registration_data.id"), nullable=False)
    registrationData: Mapped["RegistrationDataORM"] = relationship("RegistrationDataORM")
