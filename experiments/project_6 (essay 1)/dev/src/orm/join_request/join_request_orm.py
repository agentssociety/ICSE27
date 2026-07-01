from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class JoinRequestORM(Base):
    __tablename__ = "join_request"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    requestId: Mapped[str] = mapped_column(String, nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    groupId: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    groupMembership_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
