from __future__ import annotations

from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Base


class DataAtRestEncryptionORM(Base):
    __tablename__ = "data_at_rest_encryption"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    encrypted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey("resource.id"), nullable=False)
    resource: Mapped["ResourceORM"] = relationship("ResourceORM")