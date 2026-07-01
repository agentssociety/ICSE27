from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class BookmarkORM(Base):
    __tablename__ = "bookmark"

    userId: Mapped[str] = mapped_column(String, primary_key=True)
    postId: Mapped[str] = mapped_column(String, nullable=False)