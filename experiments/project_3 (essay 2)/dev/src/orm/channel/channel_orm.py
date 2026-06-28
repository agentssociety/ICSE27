from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class ChannelORM(Base):
    __tablename__ = "channel"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channelId: Mapped[str] = mapped_column(String, nullable=False)
    channelType: Mapped[str] = mapped_column(String, nullable=False)
