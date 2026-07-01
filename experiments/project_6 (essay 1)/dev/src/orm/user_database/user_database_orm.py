from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class User_DatabaseORM(Base):
    __tablename__ = "user_database"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
