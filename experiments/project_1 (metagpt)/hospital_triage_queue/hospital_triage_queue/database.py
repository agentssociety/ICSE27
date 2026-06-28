"""Database module for Hospital Triage Queue System.

This module provides an asynchronous SQLite database interface for persisting
patient data. It uses aiosqlite for non-blocking database operations.
"""

import aiosqlite
from datetime import datetime
from typing import List, Optional

from models import Patient


class Database:
    """Asynchronous SQLite database manager for patient records.

    Handles CRUD operations and table management for the triage queue system.
    Uses aiosqlite for async compatibility with FastAPI.

    Attributes:
        db_path: Path to the SQLite database file.
        conn: The aiosqlite connection object (None until connected).
    """

    def __init__(self, db_path: str = "triage.db") -> None:
        """Initialize the database manager.

        Args:
            db_path: File path for the SQLite database. Defaults to 'triage.db'.
        """
        self.db_path: str = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> None:
        """Establish the database connection and create tables if needed."""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self.create_tables()

    async def create_tables(self) -> None:
        """Create the patients table if it does not exist.

        The table schema matches the Patient model fields.
        """
        if self.conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")

        query = """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            urgency INTEGER NOT NULL CHECK(urgency >= 1 AND urgency <= 5),
            triage_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL
        )
        """
        await self.conn.execute(query)
        await self.conn.commit()

    async def insert_patient(self, patient: Patient) -> int:
        """Insert a new patient record into the database.

        Args:
            patient: Patient object to insert.

        Returns:
            int: The auto-generated ID of the inserted patient.

        Raises:
            RuntimeError: If database is not connected.
        """
        if self.conn is None:
            raise RuntimeError("Database not connected.")

        query = """
        INSERT INTO patients (name, symptoms, urgency, triage_time, arrival_time)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = await self.conn.execute(query, (
            patient.name,
            patient.symptoms,
            patient.urgency,
            patient.triage_time.isoformat(),
            patient.arrival_time.isoformat(),
        ))
        await self.conn.commit()
        return cursor.lastrowid

    async def update_patient(self, patient: Patient) -> None:
        """Update an existing patient record.

        Args:
            patient: Patient object with updated fields. Must have a valid id.

        Raises:
            RuntimeError: If database is not connected.
        """
        if self.conn is None:
            raise RuntimeError("Database not connected.")

        query = """
        UPDATE patients
        SET name = ?, symptoms = ?, urgency = ?, triage_time = ?, arrival_time = ?
        WHERE id = ?
        """
        await self.conn.execute(query, (
            patient.name,
            patient.symptoms,
            patient.urgency,
            patient.triage_time.isoformat(),
            patient.arrival_time.isoformat(),
            patient.id,
        ))
        await self.conn.commit()

    async def delete_patient(self, patient_id: int) -> None:
        """Delete a patient record by ID.

        Args:
            patient_id: ID of the patient to delete.

        Raises:
            RuntimeError: If database is not connected.
        """
        if self.conn is None:
            raise RuntimeError("Database not connected.")

        query = "DELETE FROM patients WHERE id = ?"
        await self.conn.execute(query, (patient_id,))
        await self.conn.commit()

    async def fetch_all(self) -> List[Patient]:
        """Retrieve all patient records from the database.

        Converts ISO datetime strings back to datetime objects.

        Returns:
            List[Patient]: List of Patient objects sorted by urgency and triage time.

        Raises:
            RuntimeError: If database is not connected.
            ValueError: If stored datetime strings cannot be parsed.
        """
        if self.conn is None:
            raise RuntimeError("Database not connected.")

        query = "SELECT * FROM patients ORDER BY urgency ASC, triage_time ASC"
        cursor = await self.conn.execute(query)
        rows = await cursor.fetchall()

        patients: List[Patient] = []
        for row in rows:
            try:
                triage_time = (
                    datetime.fromisoformat(row["triage_time"])
                    if row["triage_time"]
                    else None
                )
                arrival_time = (
                    datetime.fromisoformat(row["arrival_time"])
                    if row["arrival_time"]
                    else None
                )
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid datetime format in database for patient id {row['id']}: {exc}"
                ) from exc

            patient = Patient(
                id=row["id"],
                name=row["name"],
                symptoms=row["symptoms"],
                urgency=row["urgency"],
                triage_time=triage_time,
                arrival_time=arrival_time,
            )
            patients.append(patient)
        return patients

    async def close(self) -> None:
        """Close the database connection if open."""
        if self.conn is not None:
            await self.conn.close()
            self.conn = None

