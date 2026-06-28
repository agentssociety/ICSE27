"""Main application module for Hospital Triage Queue System.

This module implements the FastAPI web application that serves as the backend
for the hospital triage queue system. It handles patient registration, dequeue,
re-triage operations, and provides real-time queue data to the dashboard.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from database import Database
from dashboard import DashboardAPI
from queue_manager import QueueManager
from triage_rules import TriageRuleEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Pydantic models for request/response validation
class RegisterPatientRequest(BaseModel):
    """Request model for patient registration endpoint."""
    name: str = Field(..., min_length=1, description="Patient's full name")
    symptoms: str = Field(..., min_length=1, description="Description of symptoms")
    manual_urgency: Optional[int] = Field(
        None, ge=1, le=5, description="Optional manual urgency override (1-5)"
    )


class DequeueResponse(BaseModel):
    """Response model for dequeue operation."""
    success: bool
    patient: Optional[Dict[str, Any]] = None
    message: str


class ReTriageRequest(BaseModel):
    """Request model for re-triage endpoint."""
    patient_id: int = Field(..., gt=0, description="ID of patient to re-triage")
    new_urgency: int = Field(..., ge=1, le=5, description="New urgency level (1-5)")


class QueueResponse(BaseModel):
    """Response model for queue data."""
    patients: List[Dict[str, Any]]
    total_patients: int
    average_wait_time: float


class StatsResponse(BaseModel):
    """Response model for statistics."""
    total_patients: int
    average_wait_time: float
    urgency_distribution: Dict[str, int]


# Global application state
class AppState:
    """Holds application-wide state and dependencies."""
    def __init__(self) -> None:
        self.database: Optional[Database] = None
        self.rule_engine: Optional[TriageRuleEngine] = None
        self.queue_manager: Optional[QueueManager] = None
        self.dashboard: Optional[DashboardAPI] = None


app_state: AppState = AppState()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Application lifespan manager for startup and shutdown events.
    
    Args:
        app: The FastAPI application instance.
    """
    # Startup
    logger.info("Starting Hospital Triage Queue System...")
    
    try:
        # Initialize database
        app_state.database = Database(db_path="triage.db")
        await app_state.database.connect()
        logger.info("Database connection established")
        
        # Initialize rule engine
        app_state.rule_engine = TriageRuleEngine(rule_file="rules.json")
        logger.info("Triage rule engine initialized")
        
        # Initialize queue manager
        app_state.queue_manager = QueueManager(
            db=app_state.database,
            rule_engine=app_state.rule_engine,
        )
        await app_state.queue_manager.initialize()
        logger.info("Queue manager initialized")
        
        # Initialize dashboard
        app_state.dashboard = DashboardAPI(queue=app_state.queue_manager)
        logger.info("Dashboard API initialized")
        
    except Exception as exc:
        logger.error("Failed to initialize application: %s", exc)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Hospital Triage Queue System...")
    
    if app_state.queue_manager is not None:
        try:
            await app_state.queue_manager.save_state()
            logger.info("Queue state saved")
        except Exception as exc:
            logger.error("Failed to save queue state: %s", exc)
    
    if app_state.database is not None:
        try:
            await app_state.database.close()
            logger.info("Database connection closed")
        except Exception as exc:
            logger.error("Failed to close database: %s", exc)


# Create FastAPI application
app = FastAPI(
    title="Hospital Triage Queue System API",
    description="Backend API for managing patient triage queue with real-time updates",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes
@app.post("/register", response_model=Dict[str, Any])
async def post_register(request: RegisterPatientRequest) -> Dict[str, Any]:
    """Register a new patient in the triage queue.
    
    Args:
        request: Patient registration data including name, symptoms, and optional urgency.
    
    Returns:
        dict: The registered patient data with assigned urgency.
    
    Raises:
        HTTPException: If registration fails due to invalid data or system error.
    """
    if app_state.queue_manager is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        patient = await app_state.queue_manager.add_patient(
            name=request.name,
            symptoms=request.symptoms,
            manual_urgency=request.manual_urgency,
        )
        logger.info(
            "Patient registered successfully: id=%d, name='%s'",
            patient.id, patient.name
        )
        return patient.to_dict()
    except ValueError as exc:
        logger.warning("Invalid patient registration data: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error("Failed to register patient: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/dequeue", response_model=DequeueResponse)
async def post_dequeue() -> DequeueResponse:
    """Dequeue the highest priority patient from the queue.
    
    Returns:
        DequeueResponse: Contains success status and patient data if available.
    
    Raises:
        HTTPException: If dequeue operation fails.
    """
    if app_state.queue_manager is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        patient = await app_state.queue_manager.dequeue()
        if patient is None:
            logger.info("Dequeue attempted on empty queue")
            return DequeueResponse(
                success=False,
                patient=None,
                message="Queue is empty",
            )
        
        logger.info(
            "Patient dequeued successfully: id=%d, name='%s'",
            patient.id, patient.name
        )
        return DequeueResponse(
            success=True,
            patient=patient.to_dict(),
            message=f"Patient '{patient.name}' removed from queue",
        )
    except Exception as exc:
        logger.error("Failed to dequeue patient: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/re_triage", response_model=Dict[str, Any])
async def post_re_triage(request: ReTriageRequest) -> Dict[str, Any]:
    """Update the urgency level for an existing patient.
    
    Args:
        request: Contains patient_id and new_urgency values.
    
    Returns:
        dict: The updated patient data.
    
    Raises:
        HTTPException: If patient not found or update fails.
    """
    if app_state.queue_manager is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        patient = await app_state.queue_manager.re_triage(
            patient_id=request.patient_id,
            new_urgency=request.new_urgency,
        )
        if patient is None:
            logger.warning(
                "Patient not found for re-triage: id=%d",
                request.patient_id
            )
            raise HTTPException(
                status_code=404,
                detail=f"Patient with id {request.patient_id} not found",
            )
        
        logger.info(
            "Patient re-triaged successfully: id=%d, new urgency=%d",
            patient.id, patient.urgency
        )
        return patient.to_dict()
    except ValueError as exc:
        logger.warning("Invalid re-triage data: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to re-triage patient: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/queue", response_model=QueueResponse)
async def get_queue() -> QueueResponse:
    """Get the current queue with computed waiting times.
    
    Returns:
        QueueResponse: Contains list of patients, total count, and average wait time.
    
    Raises:
        HTTPException: If fetching queue data fails.
    """
    if app_state.dashboard is None or app_state.queue_manager is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        data = app_state.dashboard.get_queue_data()
        return QueueResponse(
            patients=data.get("patients", []),
            total_patients=data.get("total_patients", 0),
            average_wait_time=data.get("average_wait_time", 0.0),
        )
    except Exception as exc:
        logger.error("Failed to get queue data: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """Get queue statistics including urgency distribution.
    
    Returns:
        StatsResponse: Contains total patients, average wait time, and urgency breakdown.
    
    Raises:
        HTTPException: If fetching statistics fails.
    """
    if app_state.dashboard is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        stats = app_state.dashboard.get_stats()
        return StatsResponse(
            total_patients=stats.get("total_patients", 0),
            average_wait_time=stats.get("average_wait_time", 0.0),
            urgency_distribution=stats.get("urgency_distribution", {}),
        )
    except Exception as exc:
        logger.error("Failed to get queue stats: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint to verify system status.
    
    Returns:
        dict: System health status with queue information.
    """
    if app_state.queue_manager is None:
        return {
            "status": "unhealthy",
            "message": "System not initialized",
        }
    
    return {
        "status": "healthy",
        "queue_length": app_state.queue_manager.get_queue_length(),
        "next_patient_id": app_state.queue_manager.get_next_id(),
    }


@app.get("/rules", response_model=Dict[str, int])
async def get_rules() -> Dict[str, int]:
    """Get the current triage rules configuration.
    
    Returns:
        dict: Current symptom-to-urgency mapping.
    
    Raises:
        HTTPException: If rule engine is not initialized.
    """
    if app_state.rule_engine is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    return app_state.rule_engine.get_rules()


@app.get("/patients/{patient_id}", response_model=Dict[str, Any])
async def get_patient(patient_id: int) -> Dict[str, Any]:
    """Get a specific patient by ID.
    
    Args:
        patient_id: The ID of the patient to retrieve.
    
    Returns:
        dict: Patient data if found.
    
    Raises:
        HTTPException: If patient not found or system error.
    """
    if app_state.queue_manager is None:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        patient = app_state.queue_manager.get_patient(patient_id)
        if patient is None:
            raise HTTPException(
                status_code=404,
                detail=f"Patient with id {patient_id} not found",
            )
        return patient.to_dict()
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Failed to get patient %d: %s", patient_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error")


# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


def create_app() -> FastAPI:
    """Factory function to create the FastAPI application.
    
    This allows for testing and configuration flexibility.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    return app


if __name__ == "__main__":
    import uvicorn
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
