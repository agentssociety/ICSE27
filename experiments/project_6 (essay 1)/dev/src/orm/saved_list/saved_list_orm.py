from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class SavedListORM(Base):
    __tablename__ = "saved_list"

    userId: Mapped[str] = mapped_column(String, primary_key=True)