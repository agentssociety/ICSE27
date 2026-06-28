from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class UserAuthenticationSystemORM(Base):
    __tablename__ = "user_authentication_system"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sessionToken: Mapped[str] = mapped_column(String, nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
