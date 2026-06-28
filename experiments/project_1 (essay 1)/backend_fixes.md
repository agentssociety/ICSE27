# Backend Fixes Report

## What Was Fixed

### 1. `alembic/env.py` — Removed conflicting stub file
**File:** `alembic/env.py`  
**Error:** `ModuleNotFoundError: No module named 'alembic.env'` (blocking, flagged by the module-checker)  
**Root cause:** The `alembic/` directory at the project root contained a stub `env.py` with only a comment. Because the directory name collides with the installed `alembic` package, Python resolves `import alembic` to the installed package, then fails to find `env` inside it. The file was unreachable and unimportable.  
**Fix:** Deleted `alembic/env.py`. The real migration env is at `migrations/env.py`, and `alembic.ini` already points `script_location = migrations`, so nothing in alembic's toolchain used the stub.

---

### 2. `src/dto/patient/patient_dto.py` — Missing `UUID` import
**Error:** `NameError` at instantiation — `PatientCreate is not fully defined; you should define UUID`  
**Root cause:** The file imported `import uuid` (the module) but used `UUID` (the class) as a type annotation. With `from __future__ import annotations`, Pydantic defers evaluation, so class definition succeeded but runtime construction of any `PatientCreate` instance raised an error.  
**Fix:** Replaced `import uuid` with `from uuid import UUID`. Also updated `PatientCreate.patientQueue_id` to be `Optional[int]` (consistent with the ORM change in fix #8).

---

### 3. `src/dto/patient_queue/patient_queue_dto.py` — Same missing `UUID` import
**Error:** Same `NameError` as above for `PatientQueueCreate`.  
**Fix:** Replaced `import uuid` with `from uuid import UUID`.

---

### 4. `src/orm/urgency_level/urgency_level_orm.py` — Stub dataclass instead of SQLAlchemy model
**Error:** `AttributeError: 'UrgencyLevelORM' object has no attribute 'model_validate'` — the repo called SQLAlchemy session methods and Pydantic's `model_validate()` on a plain dataclass.  
**Root cause:** The ORM class was generated as `@dataclass class UrgencyLevelORM: pass` — no `__tablename__`, no columns, not mapped to any table. Every DB call through `SQLAlchemyUrgencyLevelRepository` would crash.  
**Fix:** Rewrote `UrgencyLevelORM` as a proper `DeclarativeBase` mapped class with `__tablename__ = "urgency_level"` and columns: `id` (PK), `level` (String, unique), `sort_order` (Integer).

---

### 5. `src/dto/urgency_level/urgency_level_dto.py` — Plain dataclasses instead of Pydantic models
**Error:** `AttributeError: 'UrgencyLevelResponse' object has no attribute 'model_validate'`  
**Root cause:** `UrgencyLevelResponse`, `UrgencyLevelCreateRequest`, and `UrgencyLevelUpdateRequest` were `@dataclass` classes. The repository called `.model_validate()` and `.model_dump()` on them, which are Pydantic-only methods.  
**Fix:** Converted all three to `pydantic.BaseModel` subclasses with `ConfigDict(from_attributes=True)` so the repo's ORM-to-DTO mapping works correctly.

---

### 6. `src/orm/__init__.py` — `UrgencyLevelORM` not registered
**Error:** The `urgency_level` table was never seen by Alembic or `Base.metadata.create_all()`.  
**Root cause:** The ORM init file imported all entity ORMs for side-effect registration, but `UrgencyLevelORM` was missing because it was a stub.  
**Fix:** Added `from src.orm.urgency_level.urgency_level_orm import UrgencyLevelORM  # noqa: F401`.

---

### 7. `migrations/env.py` — Wrong `alembic.ini` path
**Error:** `FileNotFoundError` when running any `alembic` CLI command (`alembic upgrade head`, `alembic revision`, etc.).  
**Root cause:** Line 30 constructed the config path as `_current_dir / 'alembic.ini'` where `_current_dir` is the `migrations/` directory. But `alembic.ini` lives one level up at the project root.  
**Fix:** Changed to `_current_dir.parent / 'alembic.ini'`.

---

### 8. `src/api/dashboard/dashboard_router.py` — `response_model=list[dict]` on a non-list return
**Error:** FastAPI validation error at runtime — the endpoint returned a single `dict` but the declared `response_model` was `list[dict]`.  
**Root cause:** The generated stub set `response_model=list[dict]` but the implementation returned `{"queue_id": ..., "message": ..., "status": ...}` (a plain dict).  
**Fix:** Removed the `response_model` annotation from the overview endpoint so FastAPI passes the dict through without validation conflict.

---

### 9. `src/orm/patient/patient_orm.py` — Missing triage-critical domain fields
**Error:** Triage data (patient state, arrival time, urgency level) was never persisted to the database.  
**Root cause:** `PatientORM` only had `id`, `patientId`, and `patientQueue_id`. The core domain fields required by every user story — `state` (RecordState), `arrival_time` (DateTime), `urgency_level` (int) — were absent from the ORM model and therefore not written to or read from the DB. Additionally, `patientQueue_id` was `NOT NULL`, conflicting with the domain model where a patient can exist before being assigned to a queue.  
**Fix:** Added `state` (String), `arrival_time` (DateTime), `urgency_level` (Integer, default 99) columns. Changed `patientQueue_id` to `nullable=True`. Updated `PatientCreate`/`PatientResponse` DTOs accordingly.

---

### 10. `src/domain/urgency_level/UrgencyLevel.py` — Duplicate `notify` method
**Error:** Silently broken — Python silently drops the first definition, so `MedicalStaff.notify(patient_ID, priority_highest)` was unreachable.  
**Root cause:** `MedicalStaff` had two `def notify(...)` methods with different parameter names (`priority_highest` and `priority_high`). Python only keeps the last definition.  
**Fix:** Merged both into a single `def notify(self, patient_ID: Any, priority: Any) -> None`.

---

## What the Backend Development Was Missing

### Domain coverage gaps
- **`urgency_level` had no persistence layer.** The domain `UrgencyLevel` enum is used in every service but there was no working ORM table, no Pydantic DTOs, and no functional CRUD repository for it. The full stack (ORM → DTO → repo → router) existed structurally but was broken end-to-end.
- **`PatientORM` did not store the data needed for triage.** Arrival time and urgency level — the two fields the queue-sort algorithm depends on — were never saved to the database. This made the sort/dequeue logic correct in memory but impossible to restore after a restart.

### Missing ORM registrations
- `UrgencyLevelORM` was not registered in `src/orm/__init__.py`, so `Base.metadata.create_all()` and Alembic would never create the `urgency_level` table.

### Alembic misconfiguration
- The `alembic.ini` file path in `migrations/env.py` pointed into the `migrations/` subdirectory instead of the project root. Any `alembic` CLI invocation would raise `FileNotFoundError`.
- An orphan `alembic/env.py` stub shadowed the installed `alembic` package for the module-checker, causing a persistent `ModuleNotFoundError: No module named 'alembic.env'` that was flagged as blocking.

### Type safety / runtime correctness
- Two DTO files (`patient_dto.py`, `patient_queue_dto.py`) used `UUID` without importing it. `from __future__ import annotations` hid the error at class-definition time, but every attempt to instantiate a `PatientCreate` or `PatientQueueCreate` would crash at runtime.
- DTO classes for `UrgencyLevel` were plain dataclasses instead of Pydantic `BaseModel` subclasses, breaking the `.model_validate()` / `.model_dump()` calls in the repository layer.

### API contract errors
- The dashboard overview endpoint declared `response_model=list[dict]` but returned a single `dict`, guaranteeing a FastAPI validation error on every call.

### Code correctness
- `MedicalStaff.notify` was defined twice with different signatures. The first definition was silently discarded by Python, meaning the "notify highest priority" variant was unreachable.
