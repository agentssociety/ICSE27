from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base

"""
Orm layer for the Transaction domain class

Package: orm.transaction
Layer: orm
Related tasks: #90, #92, #93
Requirement coverage:
- Enforce daily transaction limits
- Detect Suspicious Transaction Patterns
- Admin Interface for Flagged Transactions Review
"""

class TransactionORM(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    accountId: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(20))
    userId: Mapped[str] = mapped_column(String(36))
