from __future__ import annotations

from typing import Any
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

"""
Orm layer for the Queue domain class

Package: orm.queue
Layer: orm
Related tasks: #55, #56, #57, #58
Requirement coverage:
- Order Queue by Urgency and Time
- Automatically Reorder Queue on Change
- Take Next Patient from Queue
- Real-time live dashboard displaying urgency and wait time
"""

Base = declarative_base()

class QueueORM(Base):
    __tablename__ = "queue"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    urgency = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)