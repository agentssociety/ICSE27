from __future__ import annotations

from typing import Any
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from sqlalchemy.sql import func
import enum

from src.config.database import Base

"""
Orm layer for the TransfusionRequest domain class

Package: orm.transfusion_request
Layer: orm
Related tasks: #33, #34, #35, #38
Requirement coverage:
- Accept and Store Transfusion Requests
- Exact ABO/Rh Match First
- Automated Blood Unit Reservation and Release
- Dashboard displaying current stock levels, expiration warnings, and transfusion requests
"""

class TransfusionRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"

class TransfusionRequestORM(Base):
    __tablename__ = "transfusion_requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(50), nullable=False)
    blood_type = Column(String(10), nullable=False)
    rh_factor = Column(String(5), nullable=False)
    units_required = Column(Integer, nullable=False)
    priority = Column(String(20), nullable=False, default="normal")
    status = Column(SqlEnum(TransfusionRequestStatus), nullable=False, default=TransfusionRequestStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(String(500), nullable=True)