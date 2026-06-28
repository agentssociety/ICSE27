"""Queue manager for Hospital Triage Queue System.

This module implements the core queue management logic including patient
registration, dequeue, re-triage, and queue ordering. It uses an asyncio lock
to ensure thread-safe operations on the queue.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict

from models import Patient
from database import Database
from triage_rules import TriageRuleEngine

logger = logging.getLogger(__name__)


class QueueManager:
    """Manages the patient queue with thread-safe operations.

    This class handles all queue mutations including adding patients,
    dequeuing the highest priority patient, re-triaging existing patients,
    and maintaining the sorted order. Uses an asyncio lock for concurrency safety.

    Attributes:
        _queue: Sorted list of Patient objects in the queue.
        _next_id: Auto-incrementing ID counter for new patients.
        _lock: Asyncio lock for thread-safe queue operations.
        db: Database instance for persistence.
    """

    def __init__(
        self,
        db: Database,
        rule_engine: Optional[TriageRuleEngine] = None
    ) -> None:
        """Initialize the queue manager.

        Args:
            db: Database instance for persistent storage.
            rule_engine: Triage rule engine for automatic urgency assignment.
                        If None, a default engine will be created.
        """
        self._queue: List[Patient] = []
        self._next_id: int = 1
        self._lock: asyncio.Lock = asyncio.Lock()
        self.db: Database = db
        self._rule_engine: TriageRuleEngine = rule_engine or TriageRuleEngine()
        self._initialized: bool = False

    async def initialize(self) -> None:
        """Load existing patients from database on startup.

        This method should be called once during application startup to
        restore the queue state from persistent storage.
        """
        if self._initialized:
            return

        try:
            patients = await self.db.fetch_all()
            self._queue = patients
            if patients:
                # Find the maximum ID to continue from
                max_id = max(p.id for p in patients)
                self._next_id = max_id + 1
            self._sort_queue()
            self._initialized = True
            logger.info(
                "Queue initialized with %d patients from database",
                len(self._queue)
            )
        except Exception as exc:
            logger.error("Failed to initialize queue from database: %s", exc)
            self._initialized = True  # Still mark as initialized to prevent retry

    async def add_patient(
        self,
        name: str,
        symptoms: str,
        manual_urgency: Optional[int] = None
    ) -> Patient:
        """Register a new patient and add them to the queue.

        Args:
            name: Patient's full name.
            symptoms: Description of symptoms.
            manual_urgency: Optional override for urgency level (1-5).
                          If None, urgency is assigned by the rule engine.

        Returns:
            Patient: The newly created patient object.

        Raises:
            ValueError: If input data is invalid.
        """
        if not name or not isinstance(name, str):
            raise ValueError("Patient name must be a non-empty string")
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("Symptoms must be a non-empty string")

        async with self._lock:
            # Determine urgency
            if manual_urgency is not None:
                if not 1 <= manual_urgency <= 5:
                    raise ValueError(
                        f"Urgency must be between 1 and 5, got {manual_urgency}"
                    )
                urgency = manual_urgency
            else:
                urgency = self._rule_engine.assign_urgency(symptoms)

            # Create patient
            now = datetime.now(timezone.utc)
            patient = Patient(
                id=self._next_id,
                name=name,
                symptoms=symptoms,
                urgency=urgency,
                triage_time=now,
                arrival_time=now,
            )
            self._next_id += 1

            # Insert into database
            db_id = await self.db.insert_patient(patient)
            # Update patient ID with the one from database
            patient.id = db_id

            # Add to queue and sort
            self._queue.append(patient)
            self._sort_queue()

            logger.info(
                "Patient registered: id=%d, name='%s', urgency=%d",
                patient.id, patient.name, patient.urgency
            )
            return patient

    async def dequeue(self) -> Optional[Patient]:
        """Remove and return the highest priority patient from the queue.

        Returns:
            Patient: The patient with highest priority, or None if queue is empty.
        """
        async with self._lock:
            if not self._queue:
                logger.info("Dequeue attempted on empty queue")
                return None

            patient = self._queue.pop(0)

            # Remove from database
            await self.db.delete_patient(patient.id)

            logger.info(
                "Patient dequeued: id=%d, name='%s', urgency=%d",
                patient.id, patient.name, patient.urgency
            )
            return patient

    async def re_triage(
        self,
        patient_id: int,
        new_urgency: int
    ) -> Optional[Patient]:
        """Update the urgency level for an existing patient.

        This triggers a re-sort of the queue and updates the triage time.

        Args:
            patient_id: ID of the patient to re-triage.
            new_urgency: New urgency level (1-5).

        Returns:
            Patient: The updated patient object, or None if patient not found.

        Raises:
            ValueError: If new_urgency is out of valid range.
        """
        if not 1 <= new_urgency <= 5:
            raise ValueError(
                f"Urgency must be between 1 and 5, got {new_urgency}"
            )

        async with self._lock:
            patient = self._find_patient_by_id(patient_id)
            if patient is None:
                logger.warning("Patient not found for re-triage: id=%d", patient_id)
                return None

            # Update urgency and triage time
            old_urgency = patient.urgency
            patient.urgency = new_urgency
            patient.triage_time = datetime.now(timezone.utc)

            # Update in database
            await self.db.update_patient(patient)

            # Re-sort the queue
            self._sort_queue()

            logger.info(
                "Patient re-triaged: id=%d, urgency %d -> %d",
                patient_id, old_urgency, new_urgency
            )
            return patient

    def get_queue(self) -> List[Dict]:
        """Get the current queue with computed waiting times.

        Returns:
            List[Dict]: List of patient dictionaries with waiting times.
        """
        return [patient.to_dict() for patient in self._queue]

    def get_patient(self, patient_id: int) -> Optional[Patient]:
        """Get a specific patient by ID without modifying the queue.

        Args:
            patient_id: ID of the patient to find.

        Returns:
            Patient: The patient object if found, None otherwise.
        """
        return self._find_patient_by_id(patient_id)

    def get_patients_by_urgency(self, urgency: int) -> List[Patient]:
        """Get all patients with a specific urgency level.

        Args:
            urgency: Urgency level to filter by (1-5).

        Returns:
            List[Patient]: List of patients with the specified urgency.
        """
        if not 1 <= urgency <= 5:
            raise ValueError(f"Urgency must be between 1 and 5, got {urgency}")
        return [p for p in self._queue if p.urgency == urgency]

    def get_queue_length(self) -> int:
        """Get the current number of patients in the queue.

        Returns:
            int: Number of patients currently in queue.
        """
        return len(self._queue)

    def get_stats(self) -> Dict:
        """Get queue statistics.

        Returns:
            Dict: Statistics including total patients and average wait time.
        """
        total = len(self._queue)
        if total == 0:
            return {
                "total_patients": 0,
                "average_wait_time": 0.0,
                "urgency_distribution": {},
            }

        # Calculate average wait time
        total_wait_seconds = sum(
            p._compute_waiting_seconds() for p in self._queue
        )
        avg_wait = total_wait_seconds / total

        # Calculate urgency distribution
        urgency_dist: Dict[str, int] = {}
        for p in self._queue:
            key = f"urgency_{p.urgency}"
            urgency_dist[key] = urgency_dist.get(key, 0) + 1

        return {
            "total_patients": total,
            "average_wait_time": round(avg_wait, 1),
            "urgency_distribution": urgency_dist,
        }

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            bool: True if queue has no patients, False otherwise.
        """
        return len(self._queue) == 0

    def _sort_queue(self) -> None:
        """Sort the queue by priority.

        Patients are sorted primarily by urgency level (1 most urgent),
        and secondarily by triage time (earlier first). Uses the Patient
        __lt__ method for comparison.
        """
        self._queue.sort()
        logger.debug("Queue sorted: %d patients in queue", len(self._queue))

    def _find_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        """Find a patient in the queue by their ID.

        Args:
            patient_id: The patient ID to search for.

        Returns:
            Patient: The patient if found, None otherwise.
        """
        for patient in self._queue:
            if patient.id == patient_id:
                return patient
        return None

    def clear_queue(self) -> int:
        """Clear all patients from the queue (for testing/emergency).

        Returns:
            int: Number of patients cleared from the queue.
        """
        count = len(self._queue)
        self._queue.clear()
        logger.warning("Queue cleared: %d patients removed", count)
        return count

    def get_next_id(self) -> int:
        """Get the next available patient ID without incrementing.

        Returns:
            int: The next patient ID that would be assigned.
        """
        return self._next_id

    async def save_state(self) -> None:
        """Persist the current queue state to the database.

        This method ensures all patients in the queue are synchronized
        with the database.
        """
        async with self._lock:
            for patient in self._queue:
                try:
                    await self.db.update_patient(patient)
                except Exception as exc:
                    logger.error(
                        "Failed to save patient id=%d: %s",
                        patient.id, exc
                    )
            logger.debug("Queue state saved: %d patients", len(self._queue))

    async def load_state(self) -> None:
        """Load queue state from the database.

        This is an alias for initialize() for clarity in some contexts.
        """
        await self.initialize()

    def __len__(self) -> int:
        """Get the queue length using len().

        Returns:
            int: Number of patients in the queue.
        """
        return len(self._queue)

    def __repr__(self) -> str:
        """Get string representation of the queue manager.

        Returns:
            str: Debug representation showing queue status.
        """
        return (
            f"QueueManager(patients={len(self._queue)}, "
            f"next_id={self._next_id})"
        )

    @property
    def rule_engine(self) -> TriageRuleEngine:
        """Get the triage rule engine instance.

        Returns:
            TriageRuleEngine: The rule engine used for urgency assignment.
        """
        return self._rule_engine
