from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SeparationRuleORM(Base):
    __tablename__ = "separation_rule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wakeTurbulenceSeparation: Mapped[dict] = mapped_column(JSON, nullable=False)
