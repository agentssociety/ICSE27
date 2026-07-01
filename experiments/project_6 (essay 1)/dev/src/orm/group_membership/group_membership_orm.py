from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class GroupMembershipORM(Base):
    __tablename__ = "group_membership"

    groupId: Mapped[str] = mapped_column(String, nullable=False)
    userId: Mapped[str] = mapped_column(String, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("group.id"), nullable=False)
    group: Mapped["GroupORM"] = relationship("GroupORM")