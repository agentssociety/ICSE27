from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class AuditLogResourceORM(Base):
    __tablename__ = "audit_log_resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resourceId: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
