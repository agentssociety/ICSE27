from __future__ import annotations

import pytest
from src.service.cohort_leaderboard.cohort_leaderboard_service import (
    RankedStudent, CohortLeaderboardService
)


class TestRankedStudent:
    def test_creation(self) -> None:
        rs = RankedStudent(student_id="s1", score=100.0, rank=1)
        assert rs.student_id == "s1"
        assert rs.score == 100.0
        assert rs.rank == 1


class TestCohortLeaderboardService:
    def test_view_leaderboard_empty(self) -> None:
        svc = CohortLeaderboardService()
        result = svc.viewLeaderboard("cohort_1")
        assert result == []

    def test_aggregate_and_rank_empty(self) -> None:
        svc = CohortLeaderboardService()
        result = svc.aggregateAndRank([])
        assert result == []

    def test_aggregate_and_rank_with_scores(self) -> None:
        svc = CohortLeaderboardService()
        nuggets = [
            RankedStudent(student_id="s1", score=50.0, rank=0),
            RankedStudent(student_id="s2", score=100.0, rank=0),
        ]
        result = svc.aggregateAndRank(nuggets)
        assert len(result) == 2
        assert result[0].score == 100.0  # highest first
        assert result[1].score == 50.0
        assert result[0].rank == 1

    def test_configure_leaderboard(self) -> None:
        svc = CohortLeaderboardService()
        svc.configureLeaderboard(None, {})  # Should not raise
