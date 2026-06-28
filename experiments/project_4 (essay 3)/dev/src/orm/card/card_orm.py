from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class CardORM(Base):
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cardNumber: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    authenticationAttempt_id: Mapped[int] = mapped_column(Integer, nullable=False)
