from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class AuthenticationSessionORM(Base):
    __tablename__ = "authentication_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sessionId: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    card_id: Mapped[int] = mapped_column(Integer, nullable=False)
