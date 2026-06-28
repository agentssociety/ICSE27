from __future__ import annotations

from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
import enum


class AuthenticationOutcome(str, enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class AuthenticationMethod(str, enum.Enum):
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"
    PIN_VERIFICATION = "pin_verification"
    OTHER = "other"


class AuthenticationAttemptORM(Base):
    __tablename__ = "authentication_attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    outcome: Mapped[str] = mapped_column(String(20), nullable=False)
    method: Mapped[str] = mapped_column(String(30), nullable=False, default="login")
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False, default="0.0.0.0")
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
