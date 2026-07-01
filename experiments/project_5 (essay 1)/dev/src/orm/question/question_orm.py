from __future__ import annotations

from sqlalchemy import Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class QuestionORM(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String, nullable=False, default="multiple_choice")
    difficulty_tier: Mapped[str] = mapped_column(String, nullable=False, default="beginner")
    nugget_reward_multiplier: Mapped[float] = mapped_column(Float, nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=True)
    answer_options: Mapped[list] = mapped_column(JSON, nullable=True)
    correct_answer: Mapped[str] = mapped_column(String, nullable=True)
    exam_id: Mapped[int] = mapped_column(Integer, nullable=True)
    competency_ids: Mapped[list] = mapped_column(JSON, nullable=True, default=list)
