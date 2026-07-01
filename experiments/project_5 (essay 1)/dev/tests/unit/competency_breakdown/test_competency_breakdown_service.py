from __future__ import annotations

import pytest
from src.service.competency_breakdown.competency_breakdown_service import CompetencyBreakdownService


class TestCompetencyBreakdownService:
    def test_get_breakdown_empty(self) -> None:
        svc = CompetencyBreakdownService()
        result = svc.get_breakdown("student_1", "exam_1")
        assert result == {}

    def test_calculate_competency_scores_empty(self) -> None:
        svc = CompetencyBreakdownService()
        result = svc.calculate_competency_scores({}, {})
        assert result == {}

    def test_calculate_competency_scores_all_correct(self) -> None:
        svc = CompetencyBreakdownService()
        answers = {"q1": "A", "q2": "B"}
        competencies = {"math": ["q1", "q2"]}
        result = svc.calculate_competency_scores(answers, competencies)
        assert result["math"] == 100.0

    def test_calculate_competency_scores_partial(self) -> None:
        svc = CompetencyBreakdownService()
        answers = {"q1": "A"}
        competencies = {"math": ["q1", "q2"]}
        result = svc.calculate_competency_scores(answers, competencies)
        assert result["math"] == 50.0

    def test_calculate_competency_scores_no_questions(self) -> None:
        svc = CompetencyBreakdownService()
        answers = {}
        competencies = {"math": []}
        result = svc.calculate_competency_scores(answers, competencies)
        assert result["math"] == 0.0
