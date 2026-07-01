from __future__ import annotations

import pytest
from src.domain.exam_builder.ExamBuilder import (
    ExamBuilder,
    QuestionType,
    DifficultyTier,
)
from src.domain.question import Question as QDomain


class TestExamBuilderDomain:
    def test_create_exam_builder(self) -> None:
        builder = ExamBuilder()
        assert builder is not None
        assert builder.questions == []

    def test_create_question_mc(self) -> None:
        question = QDomain(
            type=QuestionType.MULTIPLE_CHOICE,
            difficultyTier=DifficultyTier.BEGINNER,
            nuggetRewardMultiplier=1.0
        )
        assert question.type == QuestionType.MULTIPLE_CHOICE
        assert question.difficultyTier == DifficultyTier.BEGINNER
        assert question.nuggetRewardMultiplier == 1.0

    def test_create_question_drag_and_drop(self) -> None:
        question = QDomain(
            type=QuestionType.DRAG_AND_DROP,
            difficultyTier=DifficultyTier.INTERMEDIATE,
            nuggetRewardMultiplier=2.0
        )
        assert question.type == QuestionType.DRAG_AND_DROP
        assert question.difficultyTier == DifficultyTier.INTERMEDIATE
        assert question.nuggetRewardMultiplier == 2.0

    def test_create_question_code_snippet(self) -> None:
        question = QDomain(
            type=QuestionType.CODE_SNIPPET,
            difficultyTier=DifficultyTier.ADVANCED,
            nuggetRewardMultiplier=3.0
        )
        assert question.type == QuestionType.CODE_SNIPPET
        assert question.difficultyTier == DifficultyTier.ADVANCED
        assert question.nuggetRewardMultiplier == 3.0

    def test_add_competency_to_question(self) -> None:
        from src.domain.competency import Competency

        question = QDomain(
            type=QuestionType.MULTIPLE_CHOICE,
        )
        comp = Competency(id="comp1", name="Python Basics")
        question.add_competency(comp)
        assert comp in question.competencies

    def test_set_nugget_multiplier(self) -> None:
        question = QDomain(
            type=QuestionType.MULTIPLE_CHOICE,
        )
        question.set_nugget_multiplier(1.5)
        assert question.nuggetRewardMultiplier == 1.5

    def test_negative_nugget_multiplier_raises(self) -> None:
        question = QDomain(
            type=QuestionType.MULTIPLE_CHOICE,
        )
        with pytest.raises(ValueError, match="Nugget reward multiplier must be non-negative"):
            question.set_nugget_multiplier(-1.0)
