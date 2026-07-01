from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class GroupORM(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    groupName_id: Mapped[int] = mapped_column(Integer, nullable=False)
    groupResource_id: Mapped[int] = mapped_column(Integer, nullable=False)
