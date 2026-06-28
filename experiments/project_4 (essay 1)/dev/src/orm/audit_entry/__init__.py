import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.config.database import Base

class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )