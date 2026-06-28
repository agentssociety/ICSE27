"""Dashboard API for Hospital Triage Queue System.

This module provides the data aggregation layer for the frontend dashboard.
It computes waiting times, statistics, and prepares the queue data for
real-time display.
"""

import logging
from typing import Any, Dict, List, Optional

from queue_manager import QueueManager

logger = logging.getLogger(__name__)


class DashboardAPI:
    """Provides aggregated queue data and statistics for the frontend.

    This class acts as a facade over the QueueManager, computing derived
    values such as waiting times and summary statistics. It is designed to
    be injected into the FastAPI application for serving dashboard endpoints.

    Attributes:
        queue: Reference to the QueueManager instance.
    """

    def __init__(self, queue: QueueManager) -> None:
        """Initialize the dashboard API.

        Args:
            queue: An initialized QueueManager instance.
        """
        self.queue: QueueManager = queue
        logger.info("DashboardAPI initialized with queue manager")

    def get_queue_data(self) -> Dict[str, Any]:
        """Get the current queue with computed waiting times.

        This method fetches the patient list from the queue manager and
        wraps it in a standardized response format suitable for the dashboard.

        Returns:
            dict: A dictionary containing:
                - 'patients': List of patient dictionaries with waiting times.
                - 'total_patients': Number of patients in queue.
                - 'average_wait_time': Average waiting time in seconds.
        """
        try:
            patients: List[Dict[str, Any]] = self.queue.get_queue()
            total: int = self.queue.get_queue_length()
            stats: Dict[str, Any] = self.queue.get_stats()

            return {
                "patients": patients,
                "total_patients": total,
                "average_wait_time": stats.get("average_wait_time", 0.0),
            }
        except Exception as exc:
            logger.error("Failed to get queue data: %s", exc)
            return {
                "patients": [],
                "total_patients": 0,
                "average_wait_time": 0.0,
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics.

        Returns:
            dict: Statistics including:
                - 'total_patients': Number of patients in queue.
                - 'average_wait_time': Average waiting time in seconds.
                - 'urgency_distribution': Mapping of urgency levels to patient counts.
        """
        try:
            return self.queue.get_stats()
        except Exception as exc:
            logger.error("Failed to get queue stats: %s", exc)
            return {
                "total_patients": 0,
                "average_wait_time": 0.0,
                "urgency_distribution": {},
            }
