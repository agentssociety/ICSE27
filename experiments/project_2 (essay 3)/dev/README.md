# Project 8 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 27 |
| Requirements linked | 7 |
| Tasks | 7 |
| Domain classes | 3 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.blood_unit` · layer: `domain`

Path: `src/domain/blood_unit`
> Domain layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `BloodUnit.py` | `Resource`, `BloodUnit`, `Actor`, `Permission`, `State`, `BloodUnitId`, `BloodUnitCreatedEvent`, `BloodUnitUpdatedEvent` |

### `dto.blood_unit` · layer: `dto`

Path: `src/dto/blood_unit`
> Dto layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_dto.py` | `BloodUnitCreateRequest`, `BloodUnitUpdateRequest`, `BloodUnitResponse` |

### `repository.blood_unit` · layer: `repository`

Path: `src/repository/blood_unit`
> Repository layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_repository.py` | `Inventory_Management_API`, `Interface`, `IfaceKind` |

### `orm.blood_unit` · layer: `orm`

Path: `src/orm/blood_unit`
> Orm layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_orm.py` | `BloodUnitORM` |

### `infra.blood_unit` · layer: `infra`

Path: `src/infra/blood_unit`
> Infra layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_repo_impl.py` | `SQLAlchemyBloodUnitRepository` |

### `service.blood_unit` · layer: `service`

Path: `src/service/blood_unit`
> Service layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_service.py` | `BloodUnitService`, `BloodUnitServiceImpl` |

### `api.blood_unit` · layer: `api`

Path: `src/api/blood_unit`
> Api layer for the BloodUnit domain class

| File | Classes |
|------|---------|
| `blood_unit_router.py` | `BloodUnitRouter` |

### `tests.unit.blood_unit` · layer: `tests`

Path: `tests/unit/blood_unit`
> Unit tests for BloodUnit across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_blood_unit_domain.py` | — |
| `test_blood_unit_service.py` | — |
| `test_blood_unit_api.py` | — |

### `domain.transfusion_request` · layer: `domain`

Path: `src/domain/transfusion_request`
> Domain layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `TransfusionRequest.py` | `Permission`, `State`, `Actor`, `Resource`, `Transfusion_Requests_Resource`, `PatientDetail`, `BloodType`, `TransfusionRequest`, `TransfusionRequestId`, `TransfusionRequestCreatedEvent`, `TransfusionRequestUpdatedEvent` |

### `dto.transfusion_request` · layer: `dto`

Path: `src/dto/transfusion_request`
> Dto layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_dto.py` | `TransfusionRequestCreateRequest`, `TransfusionRequestUpdateRequest`, `TransfusionRequestResponse` |

### `repository.transfusion_request` · layer: `repository`

Path: `src/repository/transfusion_request`
> Repository layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_repository.py` | `IfaceKind`, `Interface`, `Transfusion_Request_Submission_API`, `Transfusion_Requests_Database` |

### `orm.transfusion_request` · layer: `orm`

Path: `src/orm/transfusion_request`
> Orm layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_orm.py` | `TransfusionRequestORM` |

### `infra.transfusion_request` · layer: `infra`

Path: `src/infra/transfusion_request`
> Infra layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_repo_impl.py` | `SQLAlchemyTransfusionRequestRepository` |

### `service.transfusion_request` · layer: `service`

Path: `src/service/transfusion_request`
> Service layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_service.py` | `REQ_BBT_01` |

### `api.transfusion_request` · layer: `api`

Path: `src/api/transfusion_request`
> Api layer for the TransfusionRequest domain class

| File | Classes |
|------|---------|
| `transfusion_request_router.py` | `TransfusionRequestRouter` |

### `tests.unit.transfusion_request` · layer: `tests`

Path: `tests/unit/transfusion_request`
> Unit tests for TransfusionRequest across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_transfusion_request_domain.py` | — |
| `test_transfusion_request_service.py` | — |
| `test_transfusion_request_api.py` | — |

### `domain.reservation` · layer: `domain`

Path: `src/domain/reservation`
> Domain layer for the Reservation domain class

| File | Classes |
|------|---------|
| `Reservation.py` | `ComponentType`, `BloodUnitStatus`, `TransfusionRequestStatus`, `Reservation`, `ReservationId`, `ReservationCreatedEvent`, `ReservationUpdatedEvent` |

### `dto.reservation` · layer: `dto`

Path: `src/dto/reservation`
> Dto layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_dto.py` | `ReservationCreateRequest`, `ReservationUpdateRequest`, `ReservationResponse` |

### `repository.reservation` · layer: `repository`

Path: `src/repository/reservation`
> Repository layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_repository.py` | `BloodInventoryDatabase`, `InventoryManagementAPI`, `BloodBankManagerUI`, `SystemClock` |

### `orm.reservation` · layer: `orm`

Path: `src/orm/reservation`
> Orm layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_orm.py` | `ReservationORM` |

### `infra.reservation` · layer: `infra`

Path: `src/infra/reservation`
> Infra layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_repo_impl.py` | `SQLAlchemyReservationRepository` |

### `service.reservation` · layer: `service`

Path: `src/service/reservation`
> Service layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_service.py` | `ReservationService`, `ReservationServiceImpl` |

### `api.reservation` · layer: `api`

Path: `src/api/reservation`
> Api layer for the Reservation domain class

| File | Classes |
|------|---------|
| `reservation_router.py` | `ReservationRouter` |

### `tests.unit.reservation` · layer: `tests`

Path: `tests/unit/reservation`
> Unit tests for Reservation across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_reservation_domain.py` | — |
| `test_reservation_service.py` | — |
| `test_reservation_api.py` | — |

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
| `test_blood_unit_flow.py` | — |
| `test_transfusion_request_flow.py` | — |
| `test_reservation_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #39 — Blood Unit Tracking

**As a** blood bank manager
**I need** to track blood units with ABO/Rh type and collection date
**So that** I can achieve full inventory management

### Details and Assumptions
* The system must store at least ABO/Rh type and collection date for each blood unit.
* Additional attributes (e.g., unit ID, expiration date) may be needed later for full inventory management.

### Acceptance Criteria

```gherkin
Given a new blood unit is received
When I record its ABO/Rh type and collection date
Then the unit is added to the inventory with the provided details
And I can view all tracked units in the inventory
```

**UML class diagram:** `experiments/project_8/class_diagram_39.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Actor`, `BloodUnit`, `Permission`, `Resource`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/repository/blood_unit/blood_unit_repository.py` | `IfaceKind`, `Inventory_Management_API` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `IfaceKind` |

---

### Task #40 — Transfusion Request Intake

**As a** blood bank technician
**I need** to accept and record transfusion requests from medical staff, including patient details and required blood type
**So that** transfusion requests are properly documented and can be processed

### Details and Assumptions
* Requests are submitted by medical staff.
* Each request includes patient details (e.g., name, ID) and required blood type.
* The system must store the request for further processing.

### Acceptance Criteria

```gherkin
Given a medical staff submits a transfusion request with patient details and required blood type
When the blood bank technician accepts and records the request
Then the request is stored in the system and is available for processing
```

**UML class diagram:** `experiments/project_8/class_diagram_40.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Actor`, `BloodType`, `PatientDetail`, `Permission`, `Resource`, `State`, `Transfusion_Requests_Resource` |
| `src/repository/blood_unit/blood_unit_repository.py` | `IfaceKind`, `Interface` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `IfaceKind`, `Interface`, `Transfusion_Request_Submission_API`, `Transfusion_Requests_Database` |
| `src/service/transfusion_request/transfusion_request_service.py` | `REQ_BBT_01` |

---

### Task #41 — Request-Unit Compatibility Matching

**As a** transfusion service user
**I need** the system to automatically match transfusion requests to compatible blood units based on ABO/Rh compatibility rules
**So that** I can ensure safe and efficient blood allocation without manual cross-checking

### Details and Assumptions
* The system will use standard ABO/Rh compatibility rules (e.g., O- is universal donor, AB+ is universal recipient)
* Compatibility rules are predefined and not user-configurable
* The matching process occurs in real-time when a transfusion request is submitted

### Acceptance Criteria

```gherkin
Given a transfusion request for a patient with a specific ABO/Rh type
When the system processes the request
Then it should only return blood units that are ABO/Rh compatible with the patient
```

**UML class diagram:** `experiments/project_8/class_diagram_41.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Actor`, `BloodUnit`, `Permission`, `Resource`, `State` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Actor`, `Permission`, `Resource`, `State`, `TransfusionRequest` |
| `src/repository/blood_unit/blood_unit_repository.py` | `IfaceKind`, `Interface` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `IfaceKind`, `Interface` |

---

### Task #42 — Reservation System with Auto-Release

**As a** blood bank manager
**I need** to reserve specific blood units for pending requests and automatically release them after a defined period or when no longer needed
**So that** blood units are efficiently allocated and not wasted

### Details and Assumptions
* Blood units have unique identifiers and types
* Pending requests have a reservation timeout period configurable by the admin
* Automatic release occurs when the request is fulfilled or cancelled, or when the timeout expires

### Acceptance Criteria

```gherkin
Given a pending request for a specific blood type and components
When the system reserves the matching blood units
Then those units are marked as reserved and unavailable for other requests

Given a reservation timeout period is configured
When the timeout expires for a reserved unit
Then that unit is automatically released and becomes available

Given a pending request is cancelled
When the cancellation is processed
Then all units reserved for that request are released
```

**UML class diagram:** `experiments/project_8/class_diagram_42.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit`, `Permission` |
| `src/domain/reservation/Reservation.py` | `BloodUnitStatus`, `ComponentType`, `Reservation`, `TransfusionRequestStatus` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Permission`, `TransfusionRequest` |
| `src/repository/reservation/reservation_repository.py` | `BloodBankManagerUI`, `BloodInventoryDatabase`, `InventoryManagementAPI`, `SystemClock` |

---

### Task #43 — Automatic Unit Expiration

**As a** inventory manager
**I need** the system to automatically mark blood units as expired when their shelf life (based on collection date) is exceeded
**So that** expired units are removed from available inventory and not used for patients

### Details and Assumptions
* The system maintains collection dates for each blood unit.
* The shelf life duration is predefined (e.g., 42 days for red blood cells).
* The expiration check runs periodically or is triggered by a scheduled job.

### Acceptance Criteria

```gherkin
Given a blood unit with a collection date that makes it past its shelf life
When the expiration check runs
Then the system marks the blood unit as expired
And removes it from the available inventory
```

**UML class diagram:** `experiments/project_8/class_diagram_43.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit`, `State` |
| `src/domain/reservation/Reservation.py` | `BloodUnitStatus` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `State` |
| `src/repository/blood_unit/blood_unit_repository.py` | `IfaceKind`, `Interface` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `IfaceKind`, `Interface` |

---

### Task #44 — Shortage Alert Threshold

**As a** inventory manager
**I need** the system to monitor inventory levels and raise alerts when the count of any ABO/Rh type drops below 5 units
**So that** I can restock blood supplies in time to meet demand

### Details and Assumptions
* The system tracks inventory by ABO/Rh blood type.
* The threshold for alerts is 5 units per type.
* Alerts can be sent via email, dashboard notification, or other standard method.

### Acceptance Criteria

```gherkin
Given the current inventory for a specific ABO/Rh type is below 5 units
When the system checks inventory levels
Then an alert is raised for that blood type
```

**UML class diagram:** `experiments/project_8/class_diagram_44.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `Resource` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `Resource` |
| `src/repository/blood_unit/blood_unit_repository.py` | `Interface` |
| `src/repository/transfusion_request/transfusion_request_repository.py` | `Interface` |

---

### Task #45 — Inventory Dashboard

**As a** blood bank manager
**I need** a dashboard displaying current stock levels, units nearing expiration, and open transfusion requests
**So that** I can efficiently manage inventory, reduce waste, and meet transfusion demands

### Details and Assumptions
* The dashboard should update in real-time to reflect current data.
* "Units nearing expiration" means blood units within a configurable threshold (e.g., 5 days) of their expiration date.
* "Open transfusion requests" are requests that have been placed but not yet fulfilled.
* The dashboard should be accessible from a web browser or internal system.

### Acceptance Criteria

```gherkin
Given I am logged in as a blood bank manager
When I open the inventory dashboard
Then I see a section titled "Current Stock Levels" listing each blood type with quantity
And I see a section titled "Units Nearing Expiration" listing each unit's type, expiration date, and days until expiry
And I see a section titled "Open Transfusion Requests" listing each request with patient ID, blood type, urgency, and request date
```

**UML class diagram:** `experiments/project_8/class_diagram_45.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/blood_unit/BloodUnit.py` | `BloodUnit`, `Permission` |
| `src/domain/transfusion_request/TransfusionRequest.py` | `BloodType`, `Permission`, `TransfusionRequest` |

---
