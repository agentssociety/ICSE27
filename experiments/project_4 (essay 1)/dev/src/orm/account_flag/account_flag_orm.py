from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class AccountFlagORM(Base):
    __tablename__ = "account_flag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    transaction_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
