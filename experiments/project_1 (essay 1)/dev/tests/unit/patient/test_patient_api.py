from __future__ import annotations

import pytest
from uuid import uuid4

from src.api.patient.patient_router import router
from src.dto.patient.patient_dto import PatientCreate, PatientUpdate, PatientResponse


def test_router_exists() -> None:
    """The patient router is defined and has routes."""
    assert router is not None
    assert len(router.routes) > 0


def test_router_has_crud_routes() -> None:
    """The router has GET, POST, PUT, DELETE routes."""
    methods = set()
    for route in router.routes:
        for method in route.methods:
            methods.add(method)
    assert "GET" in methods
    assert "POST" in methods
    assert "PUT" in methods
    assert "DELETE" in methods
