from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "user"

    userId: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)