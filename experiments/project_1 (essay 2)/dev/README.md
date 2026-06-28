# Project 2 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 11 |
| Requirements linked | 6 |
| Tasks | 6 |
| Domain classes | 1 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.patient` · layer: `domain`

Path: `src/domain/patient`
> Domain layer for the Patient domain class

| File | Classes |
|------|---------|
| `Patient.py` | `Actor`, `Permission`, `State`, `PatientRecord`, `SymptomData`, `QueueEntry`, `DataAtRestEncryption`, `Resource`, `Patient`, `PatientId`, `PatientCreatedEvent`, `PatientUpdatedEvent` |

### `dto.patient` · layer: `dto`

Path: `src/dto/patient`
> Dto layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_dto.py` | `PatientCreateRequest`, `PatientUpdateRequest`, `PatientResponse` |

### `repository.patient` · layer: `repository`

Path: `src/repository/patient`
> Repository layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_repository.py` | `Symptom_Validation_API`, `Patient_Database`, `Evaluation_Queue_System` |

### `orm.patient` · layer: `orm`

Path: `src/orm/patient`
> Orm layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_orm.py` | `PatientORM` |

### `infra.patient` · layer: `infra`

Path: `src/infra/patient`
> Infra layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_repo_impl.py` | `SQLAlchemyPatientRepository` |

### `service.patient` · layer: `service`

Path: `src/service/patient`
> Service layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_service.py` | `PatientService`, `PatientServiceImpl` |

### `api.patient` · layer: `api`

Path: `src/api/patient`
> Api layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_router.py` | `PatientRouter` |

### `tests.unit.patient` · layer: `tests`

Path: `tests/unit/patient`
> Unit tests for Patient across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_patient_domain.py` | — |
| `test_patient_service.py` | — |
| `test_patient_api.py` | — |

### `config.settings` · layer: `config`

Path: `src/config`
> Application settings, environment variables, dependency injection

| File | Classes |
|------|---------|
| `settings.py` | `Settings` |
| `dependencies.py` | `Container` |
| `database.py` | — |
| `logging.py` | — |

### `docs.api_and_deployment` · layer: `docs`

Path: `docs`
> OpenAPI documentation, admin guide, multi-city config, deployment runbook

*(no files specified)*

### `tests.integration` · layer: `tests`

Path: `tests/integration`
> End-to-end and cross-service integration tests

| File | Classes |
|------|---------|
| `test_patient_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #7 — Patient Registration with Symptoms

**As a** triage nurse
**I need** to register a new patient with their symptoms
**So that** they can be added to the queue for evaluation

### Details and Assumptions
* The triage nurse is responsible for patient intake.
* Symptoms are collected during registration.
* The patient is added to an evaluation queue.

### Acceptance Criteria

```gherkin
Given I am a triage nurse
When I register a new patient with their symptoms
Then the patient is added to the queue for evaluation
```

**UML class diagram:** `experiments/project_2/class_diagram_7.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Actor`, `DataAtRestEncryption`, `PatientRecord`, `Permission`, `QueueEntry`, `Resource`, `State`, `SymptomData` |
| `src/repository/patient/patient_repository.py` | `Evaluation_Queue_System`, `Patient_Database`, `Symptom_Validation_API` |

---

### Task #8 — Urgency Level Assignment (1-5)

**As a** triage nurse
**I need** to assign an urgency level from 1 (most urgent) to 5 (least urgent) to each patient based on their symptoms
**So that** the queue can be prioritized correctly

### Details and Assumptions
* The triage nurse will assess patient symptoms and assign a corresponding urgency level.
* The system supports urgency levels 1 through 5.

### Acceptance Criteria

```gherkin
Given a patient has been registered with symptoms
When the triage nurse assigns an urgency level from 1 to 5
Then the patient's priority in the queue is updated according to the assigned level
```

**UML class diagram:** `experiments/project_2/class_diagram_8.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient` |

---

### Task #9 — Queue Sorting by Urgency and Time

**As a** triage nurse
**I need** the queue to be sorted first by urgency level (lowest number first) and then by arrival time (earliest first)
**So that** the most critical patients are seen first

### Details and Assumptions
* Urgency level is represented by a numeric value where lower numbers indicate higher urgency.
* Arrival time is recorded as a timestamp.
* Sorting applies to the entire patient queue.

### Acceptance Criteria

```gherkin
Given the patient queue contains multiple patients with different urgency levels and arrival times
When the queue is sorted
Then patients are ordered by urgency level ascending (lowest number first)
And for patients with the same urgency level, they are ordered by arrival time ascending (earliest first)
```

**UML class diagram:** `experiments/project_2/class_diagram_9.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission`, `State` |

---

### Task #10 — Queue Reordering on New Patient or Re-triage

**As a** triage nurse
**I need** the queue to automatically reorder when a new patient is added or when an existing patient's urgency level is changed (re-triage)
**So that** the queue always reflects the current priority

### Details and Assumptions
* The queue reordering should be based on the patient's urgency level (e.g., critical, urgent, non-urgent).
* Re-triage occurs when a nurse updates a patient's urgency level after reassessment.
* The system should handle concurrent updates (e.g., multiple patients added or re-triaged at the same time) without errors.

### Acceptance Criteria

```gherkin
Given a queue with existing patients sorted by urgency level
When a new patient is added with a specific urgency level
Then the queue reorders to place the new patient in the correct position based on priority

Given a queue with a patient whose urgency level is "non-urgent"
When the nurse changes that patient's urgency level to "critical"
Then the queue reorders to move that patient to the front of the queue
```

**UML class diagram:** `experiments/project_2/class_diagram_10.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Actor`, `Patient`, `Permission` |

---

### Task #11 — Physician Takes Next Patient

**As a** physician
**I need** to take the next patient from the top of the sorted queue
**So that** I can attend to the most urgent case first

### Details and Assumptions
* The queue is sorted by patient urgency
* The physician has access to the queue system
* Taking a patient removes them from the queue

### Acceptance Criteria

```gherkin
Given the patient queue is sorted by urgency
When the physician requests the next patient
Then the system provides the patient at the top of the queue
```

**UML class diagram:** `experiments/project_2/class_diagram_11.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |

---

### Task #12 — Live Dashboard with Urgency and Wait Time

**As a** triage nurse or physician
**I need** a live dashboard that displays each patient's urgency level and estimated wait time
**So that** I can monitor the queue status in real time

### Details and Assumptions
* The dashboard is used in a hospital or clinic setting.
* It requires real‑time data updates to reflect changes in patient status.
* Patients are already triaged and assigned an urgency level.
* Estimated wait times are calculated based on current queue and resource availability.

### Acceptance Criteria

```gherkin
Given I am a triage nurse or physician
When I access the live dashboard
Then I see each patient's urgency level and estimated wait time
```

**UML class diagram:** `experiments/project_2/class_diagram_12.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Actor`, `Permission`, `Resource` |

---
