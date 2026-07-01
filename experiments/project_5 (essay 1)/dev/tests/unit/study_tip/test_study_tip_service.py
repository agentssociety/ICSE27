from __future__ import annotations

import pytest
from src.service.study_tip.study_tip_service import StudyTipService


class TestStudyTipService:
    def test_get_tips_for_competency_empty(self) -> None:
        svc = StudyTipService()
        result = svc.get_tips_for_competency("comp_1")
        assert result == []

    def test_get_tips_for_weak_areas_none_weak(self) -> None:
        svc = StudyTipService()
        scores = {"math": 80.0, "science": 70.0}
        result = svc.get_tips_for_weak_areas(scores)
        assert result == []

    def test_get_tips_for_weak_areas_with_weak(self) -> None:
        svc = StudyTipService()
        scores = {"math": 50.0, "science": 80.0}
        result = svc.get_tips_for_weak_areas(scores)
        assert len(result) == 1
        assert result[0]["competency"] == "math"
        assert result[0]["score"] == 50.0
        assert "Practice" in result[0]["tip"]
