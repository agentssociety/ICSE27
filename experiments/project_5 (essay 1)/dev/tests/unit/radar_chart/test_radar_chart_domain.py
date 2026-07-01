from __future__ import annotations

import pytest
from src.domain.radar_chart.RadarChart import RadarChart, RadarChartId, RadarChartCreatedEvent, RadarChartUpdatedEvent


class TestRadarChartDomain:
    def test_radar_chart_creation(self) -> None:
        rc = RadarChart()
        assert rc.competencies == {}
        assert rc.studentProfile is None

    def test_radar_chart_with_data(self) -> None:
        rc = RadarChart(competencies={"math": 80, "science": 75})
        assert rc.getCompetencies() == {"math": 80, "science": 75}

    def test_set_competency_valid(self) -> None:
        rc = RadarChart()
        rc.setCompetency("math", 85)
        assert rc.competencies["math"] == 85

    def test_set_competency_invalid_low(self) -> None:
        rc = RadarChart()
        with pytest.raises(ValueError, match="between 0 and 100"):
            rc.setCompetency("math", -1)

    def test_set_competency_invalid_high(self) -> None:
        rc = RadarChart()
        with pytest.raises(ValueError, match="between 0 and 100"):
            rc.setCompetency("math", 101)

    def test_set_competency_boundary(self) -> None:
        rc = RadarChart()
        rc.setCompetency("math", 0)
        rc.setCompetency("science", 100)
        assert rc.competencies["math"] == 0
        assert rc.competencies["science"] == 100

    def test_get_competencies_returns_copy(self) -> None:
        rc = RadarChart(competencies={"a": 50})
        comps = rc.getCompetencies()
        comps["b"] = 60
        assert "b" not in rc.competencies
