from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class FriendRequestORM(Base):
    __tablename__ = "friend_request"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pending: Mapped[bool] = mapped_column(Boolean, nullable=False)
    abstract_isDuplicate: Mapped[bool] = mapped_column(Boolean, nullable=False)
    abstract_validateRequest: Mapped[str] = mapped_column(Text, nullable=False)
    notification_id: Mapped[int] = mapped_column(Integer, ForeignKey("notification.id"), nullable=False)
    notification: Mapped["NotificationORM"] = relationship("NotificationORM")
