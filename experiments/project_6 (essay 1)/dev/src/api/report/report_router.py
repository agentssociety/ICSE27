from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.dto.report.report_dto import ReportCreate, ReportUpdate, ReportResponse
from src.infra.report.report_repo_impl import SQLAlchemyReportRepository

router = APIRouter()


def _repo(db: Session = Depends(get_db)) -> SQLAlchemyReportRepository:
    return SQLAlchemyReportRepository(db)


@router.get("", response_model=list[ReportResponse])
def list_reports(skip: int = 0, limit: int = 100, repo: SQLAlchemyReportRepository = Depends(_repo)):
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ReportResponse)
def get_report(item_id: int, repo: SQLAlchemyReportRepository = Depends(_repo)):
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return item


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(data: ReportCreate, repo: SQLAlchemyReportRepository = Depends(_repo)):
    return repo.create(data)


@router.put("/{item_id}", response_model=ReportResponse)
def update_report(item_id: int, data: ReportUpdate, repo: SQLAlchemyReportRepository = Depends(_repo)):
    item = repo.update(item_id, data)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(item_id: int, repo: SQLAlchemyReportRepository = Depends(_repo)):
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
