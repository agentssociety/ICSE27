from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    failed_attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    card_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

