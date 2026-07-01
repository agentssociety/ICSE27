from __future__ import annotations

import uuid

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class ActorORM(Base):
    __tablename__ = "actor"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
