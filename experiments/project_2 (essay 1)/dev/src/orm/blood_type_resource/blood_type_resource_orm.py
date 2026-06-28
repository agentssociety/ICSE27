from __future__ import annotations

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BloodTypeResourceORM(Base):
    __tablename__ = "blood_type_resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bloodType: Mapped[str] = mapped_column(String, nullable=False)
    units: Mapped[int] = mapped_column(Integer, nullable=False)