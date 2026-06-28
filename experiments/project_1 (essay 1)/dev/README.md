# Project 1 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 31 |
| Requirements linked | 6 |
| Tasks | 6 |
| Domain classes | 3 |

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
| `Patient.py` | `SeverityLevel`, `RecordState`, `Permission`, `Role`, `SymptomResource`, `Patient`, `PatientId`, `PatientCreatedEvent`, `PatientUpdatedEvent` |

### `dto.patient` · layer: `dto`

Path: `src/dto/patient`
> Dto layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_dto.py` | `PatientRegistrationDto`, `PatientRecordDto` |

### `repository.patient` · layer: `repository`

Path: `src/repository/patient`
> Repository layer for the Patient domain class

| File | Classes |
|------|---------|
| `patient_repository.py` | `PatientRepository` |

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

### `domain.patient_queue` · layer: `domain`

Path: `src/domain/patient_queue`
> Domain layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `PatientQueue.py` | `PatientQueue`, `QueueState`, `PatientQueueId`, `PatientQueueCreatedEvent`, `PatientQueueUpdatedEvent` |

### `dto.patient_queue` · layer: `dto`

Path: `src/dto/patient_queue`
> Dto layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_dto.py` | `SortingResponse`, `PatientDto` |

### `repository.patient_queue` · layer: `repository`

Path: `src/repository/patient_queue`
> Repository layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_repository.py` | `DatabasePatientQueueRepository` |

### `orm.patient_queue` · layer: `orm`

Path: `src/orm/patient_queue`
> Orm layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_orm.py` | `PatientQueueORM` |

### `infra.patient_queue` · layer: `infra`

Path: `src/infra/patient_queue`
> Infra layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_repo_impl.py` | `SQLAlchemyPatientQueueRepository` |

### `service.patient_queue` · layer: `service`

Path: `src/service/patient_queue`
> Service layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_service.py` | `PatientQueueService`, `PatientQueueServiceImpl` |

### `api.patient_queue` · layer: `api`

Path: `src/api/patient_queue`
> Api layer for the PatientQueue domain class

| File | Classes |
|------|---------|
| `patient_queue_router.py` | `SortingApiController` |

### `tests.unit.patient_queue` · layer: `tests`

Path: `tests/unit/patient_queue`
> Unit tests for PatientQueue across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_patient_queue_domain.py` | — |
| `test_patient_queue_service.py` | — |
| `test_patient_queue_api.py` | — |

### `domain.urgency_level` · layer: `domain`

Path: `src/domain/urgency_level`
> Domain layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `UrgencyLevel.py` | `PatientRecord`, `TriageNurse`, `MedicalStaff`, `PatientCareTeam`, `HealthcareFacilityManagement`, `PriorityStatus`, `Permission`, `UrgencyLevel`, `UrgencyLevelId`, `UrgencyLevelCreatedEvent`, `UrgencyLevelUpdatedEvent` |

### `dto.urgency_level` · layer: `dto`

Path: `src/dto/urgency_level`
> Dto layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_dto.py` | `UrgencyLevelCreateRequest`, `UrgencyLevelUpdateRequest`, `UrgencyLevelResponse` |

### `repository.urgency_level` · layer: `repository`

Path: `src/repository/urgency_level`
> Repository layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_repository.py` | `TriageNurseInterface`, `PatientInformationDatabase` |

### `orm.urgency_level` · layer: `orm`

Path: `src/orm/urgency_level`
> Orm layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_orm.py` | `UrgencyLevelORM` |

### `infra.urgency_level` · layer: `infra`

Path: `src/infra/urgency_level`
> Infra layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_repo_impl.py` | `SQLAlchemyUrgencyLevelRepository` |

### `service.urgency_level` · layer: `service`

Path: `src/service/urgency_level`
> Service layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_service.py` | `UrgencyLevelService`, `UrgencyLevelServiceImpl` |

### `api.urgency_level` · layer: `api`

Path: `src/api/urgency_level`
> Api layer for the UrgencyLevel domain class

| File | Classes |
|------|---------|
| `urgency_level_router.py` | `UrgencyLevelRouter` |

### `tests.unit.urgency_level` · layer: `tests`

Path: `tests/unit/urgency_level`
> Unit tests for UrgencyLevel across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_urgency_level_domain.py` | — |
| `test_urgency_level_service.py` | — |
| `test_urgency_level_api.py` | — |

### `domain.events` · layer: `domain`

Path: `src/domain/events`
> needed for dynamic requeuing on new patient or re-triage (task 4) to decouple services

*(no files specified)*

### `shared.utilities` · layer: `infra`

Path: `src/infra/utilities`
> common helpers for time calculation, validation, and cross-cutting concerns

*(no files specified)*

### `service.dashboard` · layer: `service`

Path: `src/service/dashboard`
> live dashboard (task 6) requires dedicated read model and wait time calculation

*(no files specified)*

### `api.dashboard` · layer: `api`

Path: `src/api/dashboard`
> expose dashboard endpoints, separate from patient_queue API for clarity

*(no files specified)*

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
| `test_urgency_level_flow.py` | — |
| `test_patient_queue_flow.py` | — |
| `test_patient_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #1 — Patient Registration with Symptoms

**As a** triage nurse
**I need** to register a new patient with their symptoms
**So that** they can be added to the queue for medical attention

### Details and Assumptions
* The triage nurse is responsible for initial patient intake.
* Symptoms will be collected during registration.
* The patient will be placed in a queue for medical attention.

### Acceptance Criteria

```gherkin
Given I am a triage nurse logged into the system
When I register a new patient with their symptoms
Then the patient is added to the queue for medical attention
```

**UML class diagram:** `experiments/project_1/class_diagram_1.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission`, `RecordState`, `Role`, `SeverityLevel` |
| `src/domain/patient_queue/PatientQueue.py` | `PatientQueue` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission` |
| `src/dto/patient/patient_dto.py` | `PatientRecordDto`, `PatientRegistrationDto` |

---

### Task #2 — Urgency Level Assignment

**As a** triage nurse
**I need** assign an urgency level (1-5) to each patient based on their symptoms
**So that** the most critical cases are prioritized

### Details and Assumptions
* The urgency level corresponds to severity: 1 is most urgent, 5 is least urgent.
* Symptoms are evaluated by the nurse using a standardized assessment.

### Acceptance Criteria

```gherkin
Given a patient with severe chest pain and shortness of breath
When the triage nurse evaluates symptoms
Then the assigned urgency level is 1
And the patient is marked as highest priority
```

**UML class diagram:** `experiments/project_1/class_diagram_2.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |
| `src/domain/urgency_level/UrgencyLevel.py` | `HealthcareFacilityManagement`, `MedicalStaff`, `PatientCareTeam`, `PatientRecord`, `Permission`, `PriorityStatus`, `TriageNurse` |
| `src/repository/urgency_level/urgency_level_repository.py` | `PatientInformationDatabase`, `TriageNurseInterface` |

---

### Task #3 — Queue Sorting by Urgency and Arrival Time

**As a** system  
**I need** to sort the patient queue first by urgency level (highest first) and then by arrival time (earliest first)  
**So that** patients are seen in the correct order  

### Details and Assumptions
* The system manages a patient queue.
* Urgency levels have a defined hierarchy (e.g., critical, high, medium, low).
* Arrival time is recorded for each patient.

### Acceptance Criteria

```gherkin
Given the patient queue contains multiple patients with different urgency levels and arrival times
When the sorting function is applied
Then the queue is ordered with the highest urgency patients first
And patients with the same urgency level are ordered by earliest arrival time first
```

**UML class diagram:** `experiments/project_1/class_diagram_3.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/patient_queue/patient_queue_router.py` | `SortingApiController` |
| `src/domain/patient/Patient.py` | `Patient`, `Permission`, `Role` |
| `src/domain/patient_queue/PatientQueue.py` | `PatientQueue`, `QueueState` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission`, `UrgencyLevel` |
| `src/dto/patient_queue/patient_queue_dto.py` | `PatientDto`, `SortingResponse` |
| `src/repository/patient_queue/patient_queue_repository.py` | `DatabasePatientQueueRepository` |

---

### Task #4 — Dynamic Requeuing on New Patient or Re-triage

**As a** system
**I need** to automatically re-sort the queue whenever a new patient is registered or an existing patient's urgency level is updated (re-triage)
**So that** the queue always reflects current priorities

### Details and Assumptions
* The system maintains a queue of patients.
* New patients can be registered at any time.
* Existing patients' urgency levels can be updated (re-triage).
* The queue sorting order is based on urgency/priority.
* The re-sort occurs immediately upon the triggering event.

### Acceptance Criteria

```gherkin
Given a queue containing patients sorted by urgency
When a new patient is registered
Then the queue is automatically re-sorted to include the new patient based on urgency

Given a queue containing patients sorted by urgency
When an existing patient's urgency level is updated
Then the queue is automatically re-sorted to reflect the changed urgency
```

**UML class diagram:** `experiments/project_1/class_diagram_4.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission`, `UrgencyLevel` |

---

### Task #5 — Patient Dequeue for Physician

**As a** physician
**I need** dequeue the next highest-priority patient from the queue
**So that** I can attend to them

### Details and Assumptions
* The patient queue is sorted by priority (e.g., triage level, severity).
* Dequeuing removes the patient from the queue and presents their details to the physician.
* The system ensures that the highest-priority patient is selected next.

### Acceptance Criteria

```gherkin
Given there is a queue of patients with different priorities
When the physician requests to dequeue the next patient
Then the system returns the patient with the highest priority
And that patient is removed from the queue
```

**UML class diagram:** `experiments/project_1/class_diagram_5.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Patient`, `Permission` |
| `src/domain/patient_queue/PatientQueue.py` | `PatientQueue` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission` |

---

### Task #6 — Live Dashboard with Urgency and Wait Time

**As a** hospital administrator
**I need** a live dashboard that displays each patient's urgency level and estimated wait time
**So that** staff can monitor the queue status in real time

### Details and Assumptions
* The dashboard updates in real time without manual refresh.
* Urgency levels are predefined (e.g., critical, high, medium, low).
* Estimated wait times are calculated based on current queue and resource availability.
* Accessible to authorized hospital staff only.

### Acceptance Criteria

```gherkin
Given the hospital administrator is logged into the system
When the administrator opens the live dashboard
Then the dashboard shows each patient's urgency level and estimated wait time
And the data updates automatically in real time
```

**UML class diagram:** `experiments/project_1/class_diagram_6.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/patient/Patient.py` | `Permission` |
| `src/domain/urgency_level/UrgencyLevel.py` | `Permission` |

---
