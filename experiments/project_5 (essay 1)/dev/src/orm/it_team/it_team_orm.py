from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class IT_TeamORM(Base):
    __tablename__ = "it_team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
