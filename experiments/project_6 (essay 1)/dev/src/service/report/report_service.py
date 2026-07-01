from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

from src.dto.report.report_dto import ReportCreate, ReportUpdate, ReportResponse

if TYPE_CHECKING:
    from src.infra.report.report_repo_impl import SQLAlchemyReportRepository


class ReportService(Protocol):
    def get_by_id(self, item_id: int) -> Optional[ReportResponse]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[ReportResponse]: ...
    def create(self, data: ReportCreate) -> ReportResponse: ...
    def update(self, item_id: int, data: ReportUpdate) -> Optional[ReportResponse]: ...
    def delete(self, item_id: int) -> bool: ...


class ReportServiceImpl:
    def __init__(self, repo: SQLAlchemyReportRepository) -> None:
        self._repo = repo

    def get_by_id(self, item_id: int) -> Optional[ReportResponse]:
        return self._repo.get_by_id(item_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ReportResponse]:
        return self._repo.get_all(skip=skip, limit=limit)

    def create(self, data: ReportCreate) -> ReportResponse:
        return self._repo.create(data)

    def update(self, item_id: int, data: ReportUpdate) -> Optional[ReportResponse]:
        return self._repo.update(item_id, data)

    def delete(self, item_id: int) -> bool:
        return self._repo.delete(item_id)

