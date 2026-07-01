from __future__ import annotations

import pytest
from src.service.exam_builder.exam_builder_service import (
    Operation,
)
from src.domain.exam_builder.ExamBuilder import (
    State,
    Permission,
)


class TestExamBuilderService:
    def test_operation_init(self) -> None:
        op = Operation()
        assert op.preState is None
        assert op.postState is None
        assert op.requiredPermissions is None

    def test_operation_with_state(self) -> None:
        op = Operation(
            preState=State.PRE1,
            postState=State.POST1,
            requiredPermissions={Permission.READ, Permission.WRITE}
        )
        assert op.preState == State.PRE1
        assert op.postState == State.POST1
        assert op.requiredPermissions == {Permission.READ, Permission.WRITE}
