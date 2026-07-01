from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Float, Integer, String, Text


class RewardItemORM(Base):
    __tablename__ = "reward_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cost = Column(Float, nullable=False, default=0.0)
    item_type = Column(String, nullable=False, default="virtual")
    instructor_id = Column(Integer, nullable=True)
