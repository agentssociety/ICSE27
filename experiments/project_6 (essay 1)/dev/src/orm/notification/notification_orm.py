from __future__ import annotations

from typing import Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class NotificationORM(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    like_id: Mapped[int] = mapped_column(Integer, ForeignKey("like.id"), nullable=False)
    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey("comment.id"), nullable=False)
    like: Mapped["LikeORM"] = relationship("LikeORM")
    comment: Mapped["CommentORM"] = relationship("CommentORM")
