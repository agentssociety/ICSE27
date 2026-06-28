from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.blood_unit.blood_unit_repo_impl import SQLAlchemyBloodUnitRepository
from src.infra.transfusion_request.transfusion_request_repo_impl import SQLAlchemyTransfusionRequestRepository
from src.infra.triage.triage_repo_impl import SQLAlchemyTriageRepository

router = APIRouter()


def _blood_repo(db: Session = Depends(get_db)) -> SQLAlchemyBloodUnitRepository:
    return SQLAlchemyBloodUnitRepository(db)


def _transfusion_repo(db: Session = Depends(get_db)) -> SQLAlchemyTransfusionRequestRepository:
    return SQLAlchemyTransfusionRequestRepository(db)


@router.get("/dashboard", response_model=dict)
def get_inventory_dashboard(
    blood_repo: SQLAlchemyBloodUnitRepository = Depends(_blood_repo),
    transfusion_repo: SQLAlchemyTransfusionRequestRepository = Depends(_transfusion_repo),
):
    """Get inventory dashboard with stock levels, expiring units, and pending requests."""
    stock_summary = blood_repo.get_stock_summary()
    expiring_units = blood_repo.get_expiring_soon(within_days=7)
    pending_count = transfusion_repo.count_pending()

    return {
        "stock_summary": stock_summary,
        "expiring_units_count": len(expiring_units),
        "expiring_units": [
            {
                "id": u.id,
                "bloodType": u.bloodType,
                "rhFactor": u.rhFactor,
                "expirationDate": str(u.expirationDate) if u.expirationDate else None,
            }
            for u in expiring_units
        ],
        "pending_requests_count": pending_count,
    }


def _triage_repo(db: Session = Depends(get_db)) -> SQLAlchemyTriageRepository:
    return SQLAlchemyTriageRepository(db)


@router.get("/queue/{queue_id}/overview")
def get_queue_overview(
    queue_id: str,
    triage_repo: SQLAlchemyTriageRepository = Depends(_triage_repo),
):
    stats = triage_repo.get_queue_stats()
    return {
        "queueId": queue_id,
        "patientCount": stats["count"],
        "averageWaitMinutes": stats["avg_wait"],
        "severityBreakdown": stats["severity_breakdown"],
    }
