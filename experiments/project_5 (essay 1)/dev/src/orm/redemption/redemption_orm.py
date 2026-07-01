from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, DateTime, Float, Integer
from datetime import datetime


class RedemptionORM(Base):
    __tablename__ = "redemptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    reward_item_id = Column(Integer, nullable=False)
    nuggets_spent = Column(Float, nullable=False)
    redeemed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
