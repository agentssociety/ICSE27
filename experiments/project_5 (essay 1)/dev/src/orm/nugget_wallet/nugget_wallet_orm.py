from __future__ import annotations

from src.config.database import Base
from sqlalchemy import Column, Float, Integer


class NuggetWalletORM(Base):
    __tablename__ = "nugget_wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
