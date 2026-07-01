from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, model_validator

from src.domain.question import QuestionType, DifficultyTier


class QuestionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(QuestionBase):
    type: QuestionType
    difficulty_tier: DifficultyTier = DifficultyTier.BEGINNER
    nugget_reward_multiplier: Optional[float] = None
    body: Optional[str] = None
    answer_options: Optional[list[str]] = None
    correct_answer: Optional[str] = None
    exam_id: Optional[int] = None
    competency_ids: list[int] = []


class QuestionUpdate(QuestionBase):
    type: Optional[QuestionType] = None
    difficulty_tier: Optional[DifficultyTier] = None
    nugget_reward_multiplier: Optional[float] = None
    body: Optional[str] = None
    answer_options: Optional[list[str]] = None
    correct_answer: Optional[str] = None
    exam_id: Optional[int] = None
    competency_ids: Optional[list[int]] = None


class QuestionResponse(QuestionBase):
    id: int
    type: QuestionType
    difficulty_tier: DifficultyTier = DifficultyTier.BEGINNER
    nugget_reward_multiplier: Optional[float] = None
    body: Optional[str] = None
    answer_options: Optional[list[str]] = None
    correct_answer: Optional[str] = None
    exam_id: Optional[int] = None
    competency_ids: list[int] = []

    @model_validator(mode='before')
    @classmethod
    def normalise_orm(cls, data: Any) -> Any:
        if hasattr(data, '__dict__'):
            d = {k: v for k, v in data.__dict__.items() if not k.startswith('_')}
            if 'difficultyTier' in d and 'difficulty_tier' not in d:
                d['difficulty_tier'] = d.pop('difficultyTier')
            if 'nuggetRewardMultiplier' in d and 'nugget_reward_multiplier' not in d:
                d['nugget_reward_multiplier'] = d.pop('nuggetRewardMultiplier')
            return d
        return data
