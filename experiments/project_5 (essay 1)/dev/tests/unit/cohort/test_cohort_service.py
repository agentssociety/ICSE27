from __future__ import annotations

import pytest
from src.service.cohort.cohort_service import CohortServiceImpl, CohortService


class TestCohortService:
    def test_cohort_service_interface(self) -> None:
        assert CohortServiceImpl is not None
