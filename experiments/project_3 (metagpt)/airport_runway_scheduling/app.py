"""Flask application for the flight scheduling system.

This module provides the web interface and API endpoints for managing
flights, runways, and emergency situations. It uses the Scheduler class
from the scheduler module for all scheduling logic.
"""

from __future__ import annotations

import datetime
import json
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, jsonify, render_template, request

from models import Flight
from scheduler import Scheduler


class App:
    """Main application class that wraps the Flask app and Scheduler."""

    def __init__(self) -> None:
        """Initialize the Flask application and scheduler."""
        self.app = Flask(__name__)
        self.scheduler: Scheduler = Scheduler()
        self._register_routes()

    def _register_routes(self) -> None:
        """Register all API routes with the Flask application."""
        self.app.add_url_rule(
            "/register_flight", view_func=self.register_flight_route, methods=["POST"]
        )
        self.app.add_url_rule(
            "/close_runway", view_func=self.close_runway_route, methods=["POST"]
        )
        self.app.add_url_rule(
            "/declare_emergency", view_func=self.declare_emergency_route, methods=["POST"]
        )
        self.app.add_url_rule(
            "/timetable", view_func=self.get_timetable_route, methods=["GET"]
        )

    # ------------------------------------------------------------------
    # Route Handlers
    # ------------------------------------------------------------------

    def register_flight_route(self) -> Tuple[Any, int]:
        """Handle flight registration requests.

        Expects a JSON payload with:
            - flight_id: str
            - flight_type: str ("arrival" or "departure")
            - estimated_time: str (ISO datetime)
            - is_emergency: bool (optional, default false)

        Returns:
            JSON response with registration status and slot details.
        """
        try:
            data: Dict[str, Any] = request.get_json(force=True)
            flight_id: str = data.get("flight_id", "").strip()
            flight_type: str = data.get("flight_type", "").strip()
            estimated_time_str: str = data.get("estimated_time", "").strip()
            is_emergency: bool = data.get("is_emergency", False)

            if not flight_id or not flight_type or not estimated_time_str:
                return jsonify({"error": "Missing required fields"}), 400

            if flight_type not in ("arrival", "departure"):
                return jsonify({"error": "Invalid flight_type. Must be 'arrival' or 'departure'"}), 400

            try:
                estimated_time = datetime.datetime.fromisoformat(estimated_time_str)
            except ValueError:
                return jsonify({"error": "Invalid estimated_time format. Use ISO datetime."}), 400

            flight = Flight(
                flight_id=flight_id,
                flight_type=flight_type,
                estimated_time=estimated_time,
                is_emergency=is_emergency,
            )

            success = self.scheduler.register_flight(flight)
            if not success:
                return jsonify({"error": "Failed to allocate slot. No runways available."}), 503

            slot = flight.assigned_slot
            if slot is None:
                return jsonify({"error": "Slot allocation returned None"}), 500

            response = {
                "status": "success",
                "slot": {
                    "runway": slot.runway,
                    "start_time": slot.start_time.isoformat(),
                    "end_time": slot.end_time.isoformat(),
                },
            }
            return jsonify(response), 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    def close_runway_route(self) -> Tuple[Any, int]:
        """Handle runway closure requests.

        Expects a JSON payload with:
            - runway_id: int (1 or 2)

        Returns:
            JSON response with list of delayed flights and their new slots.
        """
        try:
            data: Dict[str, Any] = request.get_json(force=True)
            runway_id: int = data.get("runway_id")

            if runway_id not in (1, 2):
                return jsonify({"error": "Invalid runway_id. Must be 1 or 2."}), 400

            delayed_flights = self.scheduler.close_runway(runway_id)

            delayed_info = []
            for flight in delayed_flights:
                slot = flight.assigned_slot
                if slot is None:
                    continue
                delayed_info.append({
                    "flight_id": flight.flight_id,
                    "new_slot": {
                        "runway": slot.runway,
                        "start_time": slot.start_time.isoformat(),
                        "end_time": slot.end_time.isoformat(),
                    },
                })

            response = {
                "status": "success",
                "delayed_flights": delayed_info,
            }
            return jsonify(response), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    def declare_emergency_route(self) -> Tuple[Any, int]:
        """Handle emergency declaration for a flight.

        Expects a JSON payload with:
            - flight_id: str

        Returns:
            JSON response with emergency slot details.
        """
        try:
            data: Dict[str, Any] = request.get_json(force=True)
            flight_id: str = data.get("flight_id", "").strip()

            if not flight_id:
                return jsonify({"error": "Missing flight_id"}), 400

            # Locate the flight in the queues
            flight = self._find_flight_by_id(flight_id)
            if flight is None:
                return jsonify({"error": f"Flight {flight_id} not found in system"}), 404

            # Handle the emergency
            slot = self.scheduler.handle_emergency(flight)
            if slot is None:
                return jsonify({"error": "Failed to allocate emergency slot. No runways available."}), 503

            response = {
                "status": "success",
                "emergency_slot": {
                    "runway": slot.runway,
                    "start_time": slot.start_time.isoformat(),
                    "end_time": slot.end_time.isoformat(),
                },
            }
            return jsonify(response), 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    def get_timetable_route(self) -> Tuple[Any, int]:
        """Render the timetable for a specific runway.

        Query parameters:
            - runway_id: int (1 or 2)

        Returns:
            HTML page with the timetable table.
        """
        try:
            runway_id_str: str = request.args.get("runway_id", "")
            if not runway_id_str:
                return jsonify({"error": "Missing runway_id query parameter"}), 400

            runway_id: int = int(runway_id_str)
            if runway_id not in (1, 2):
                return jsonify({"error": "Invalid runway_id. Must be 1 or 2."}), 400

            slots = self.scheduler.get_timetable(runway_id)
            # Prepare data for template
            timetable_data = []
            for slot in slots:
                flight_info = None
                if slot.flight is not None:
                    flight_info = {
                        "flight_id": slot.flight.flight_id,
                        "flight_type": slot.flight.flight_type,
                        "is_emergency": slot.flight.is_emergency,
                        "is_delayed": slot.flight.is_delayed,
                    }
                timetable_data.append({
                    "start_time": slot.start_time.strftime("%H:%M"),
                    "end_time": slot.end_time.strftime("%H:%M"),
                    "runway": slot.runway,
                    "flight": flight_info,
                })

            runway_status = "Open" if self.scheduler.runways[runway_id].is_open else "Closed"
            return render_template(
                "index.html",
                runway_id=runway_id,
                runway_status=runway_status,
                slots=timetable_data,
            ), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _find_flight_by_id(self, flight_id: str) -> Optional[Flight]:
        """Search for a flight by ID in both normal and emergency queues.

        Args:
            flight_id: The flight identifier to search for.

        Returns:
            The Flight object if found, else None.
        """
        # Search in normal queue (heap is a list)
        for flight in self.scheduler.flight_queue:
            if flight.flight_id == flight_id:
                return flight
        # Search in emergency queue
        for flight in self.scheduler.emergency_queue:
            if flight.flight_id == flight_id:
                return flight
        # Also check if it might already be assigned to a slot
        for runway in self.scheduler.runways.values():
            for slot in runway.slots:
                if slot.flight is not None and slot.flight.flight_id == flight_id:
                    return slot.flight
        return None

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
        """Start the Flask development server.

        Args:
            host: Host to bind to (default: all interfaces).
            port: Port to listen on (default: 5000).
            debug: Enable debug mode (default: False).
        """
        self.app.run(host=host, port=port, debug=debug)


def create_app() -> Flask:
    """Factory function to create and return the Flask app instance.

    This allows external tools (e.g., Gunicorn) to load the app via
    `app:create_app`.

    Returns:
        Configured Flask application.
    """
    app_instance = App()
    return app_instance.app


# Entry point for running directly
if __name__ == "__main__":
    app_instance = App()
    app_instance.run(debug=True)
