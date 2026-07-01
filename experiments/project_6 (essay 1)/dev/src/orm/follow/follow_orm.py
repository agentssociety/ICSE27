from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Follow domain class

Package: orm.follow
Layer: orm
Related tasks: #164
Requirement coverage:
- User Follow/Unfollow Functionality
"""


class FollowORM(Base):
    __tablename__ = "follow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    followerId: Mapped[str] = mapped_column(String, nullable=False)
    followingId: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False, default="active")
