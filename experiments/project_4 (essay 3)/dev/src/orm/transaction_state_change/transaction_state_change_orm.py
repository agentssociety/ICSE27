from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class TransactionStateChangeORM(Base):
    __tablename__ = "transaction_state_change"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
