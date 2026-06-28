# Project 7 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 37 |
| Requirements linked | 7 |
| Tasks | 7 |
| Domain classes | 4 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.flight` · layer: `domain`

Path: `src/domain/flight`
> Domain layer for the Flight domain class

| File | Classes |
|------|---------|
| `Flight.py` | `Flight`, `Direction`, `AircraftMovementLog`, `Operation`, `Actor`, `Resource`, `Permission`, `State`, `Interface`, `InterfaceKind`, `FlightId`, `FlightCreatedEvent`, `FlightUpdatedEvent` |

### `dto.flight` · layer: `dto`

Path: `src/dto/flight`
> Dto layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_dto.py` | `FlightRegistrationRequest`, `FlightRegistrationResponse` |

### `repository.flight` · layer: `repository`

Path: `src/repository/flight`
> Repository layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_repository.py` | `FlightRegistrationAPI`, `AircraftMovementLogDatabase` |

### `orm.flight` · layer: `orm`

Path: `src/orm/flight`
> Orm layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_orm.py` | `FlightORM` |

### `infra.flight` · layer: `infra`

Path: `src/infra/flight`
> Infra layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_repo_impl.py` | `SQLAlchemyFlightRepository` |

### `service.flight` · layer: `service`

Path: `src/service/flight`
> Service layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_service.py` | `FlightRegistrationService` |

### `api.flight` · layer: `api`

Path: `src/api/flight`
> Api layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_router.py` | `FlightRouter` |

### `tests.unit.flight` · layer: `tests`

Path: `tests/unit/flight`
> Unit tests for Flight across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_flight_domain.py` | — |
| `test_flight_service.py` | — |
| `test_flight_api.py` | — |

### `domain.slot` · layer: `domain`

Path: `src/domain/slot`
> Domain layer for the Slot domain class

| File | Classes |
|------|---------|
| `Slot.py` | `Permission`, `Actor`, `Resource`, `Slot`, `State`, `Operation`, `OperationSlot`, `SlotId`, `SlotCreatedEvent`, `SlotUpdatedEvent` |

### `dto.slot` · layer: `dto`

Path: `src/dto/slot`
> Dto layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_dto.py` | `SlotAllocationRequest`, `SlotAllocationResponse` |

### `repository.slot` · layer: `repository`

Path: `src/repository/slot`
> Repository layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_repository.py` | `Interface`, `Flight_Schedule_Management_API`, `Air_Traffic_Control_Console` |

### `orm.slot` · layer: `orm`

Path: `src/orm/slot`
> Orm layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_orm.py` | `SlotORM` |

### `infra.slot` · layer: `infra`

Path: `src/infra/slot`
> Infra layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_repo_impl.py` | `SQLAlchemySlotRepository` |

### `service.slot` · layer: `service`

Path: `src/service/slot`
> Service layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_service.py` | `SlotService`, `SlotServiceImpl` |

### `api.slot` · layer: `api`

Path: `src/api/slot`
> Api layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_router.py` | `SlotAllocationController` |

### `tests.unit.slot` · layer: `tests`

Path: `tests/unit/slot`
> Unit tests for Slot across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_slot_domain.py` | — |
| `test_slot_service.py` | — |
| `test_slot_api.py` | — |

### `domain.emergency_flight` · layer: `domain`

Path: `src/domain/emergency_flight`
> Domain layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `EmergencyFlight.py` | `FlightType`, `SlotStatus`, `FlightQueue`, `EmergencyFlight`, `EmergencyFlightId`, `EmergencyFlightCreatedEvent`, `EmergencyFlightUpdatedEvent` |

### `dto.emergency_flight` · layer: `dto`

Path: `src/dto/emergency_flight`
> Dto layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_dto.py` | `EmergencyRequestDTO`, `QueueStatusDTO`, `FlightDTO`, `SlotDTO` |

### `repository.emergency_flight` · layer: `repository`

Path: `src/repository/emergency_flight`
> Repository layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_repository.py` | `EmergencyHandler`, `QueueManager` |

### `orm.emergency_flight` · layer: `orm`

Path: `src/orm/emergency_flight`
> Orm layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_orm.py` | `EmergencyFlightORM` |

### `infra.emergency_flight` · layer: `infra`

Path: `src/infra/emergency_flight`
> Infra layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_repo_impl.py` | `SQLAlchemyEmergencyFlightRepository` |

### `service.emergency_flight` · layer: `service`

Path: `src/service/emergency_flight`
> Service layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_service.py` | `FlightQueueAPI`, `FlightScheduleDatabase` |

### `api.emergency_flight` · layer: `api`

Path: `src/api/emergency_flight`
> Api layer for the EmergencyFlight domain class

| File | Classes |
|------|---------|
| `emergency_flight_router.py` | `FlightQueueController` |

### `tests.unit.emergency_flight` · layer: `tests`

Path: `tests/unit/emergency_flight`
> Unit tests for EmergencyFlight across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_emergency_flight_domain.py` | — |
| `test_emergency_flight_service.py` | — |
| `test_emergency_flight_api.py` | — |

### `domain.runway` · layer: `domain`

Path: `src/domain/runway`
> Domain layer for the Runway domain class

| File | Classes |
|------|---------|
| `Runway.py` | `RunwayStatus`, `WakeTurbulenceCategory`, `PermissionLevel`, `PreState`, `PostState`, `Runway`, `Aircraft`, `TrafficData`, `SeparationRule`, `Resource`, `Permission`, `State`, `RunwayId`, `RunwayCreatedEvent`, `RunwayUpdatedEvent` |

### `dto.runway` · layer: `dto`

Path: `src/dto/runway`
> Dto layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_dto.py` | `RunwayCreateRequest`, `RunwayUpdateRequest`, `RunwayResponse` |

### `repository.runway` · layer: `repository`

Path: `src/repository/runway`
> Repository layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_repository.py` | `RunwayStatusAPI`, `AircraftAndTrafficDatabase`, `SeparationRulesDatabase` |

### `orm.runway` · layer: `orm`

Path: `src/orm/runway`
> Orm layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_orm.py` | `RunwayORM` |

### `infra.runway` · layer: `infra`

Path: `src/infra/runway`
> Infra layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_repo_impl.py` | `SQLAlchemyRunwayRepository` |

### `service.runway` · layer: `service`

Path: `src/service/runway`
> Service layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_service.py` | `System` |

### `api.runway` · layer: `api`

Path: `src/api/runway`
> Api layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_router.py` | `Actor`, `AirTrafficControlTeam`, `FlightOperationsManagement`, `SafetyComplianceOffice` |

### `tests.unit.runway` · layer: `tests`

Path: `tests/unit/runway`
> Unit tests for Runway across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_runway_domain.py` | — |
| `test_runway_service.py` | — |
| `test_runway_api.py` | — |

### `shared.exceptions` · layer: `domain`

Path: `src/domain/exceptions`
> Domain-specific exceptions (e.g., SlotOverlapException, RunwayClosedException) should be centralized for cross-domain use.

| File | Classes |
|------|---------|
| `__init__.py` | `AuthenticationException`, `AuthenticationFailedException`, `AuthorizationException`, `ConcurrentModificationException`, `DuplicateFlightNumberException`, `InvalidFlightDataException`, `InvalidFlightException`, `NoAvailableSlotException`, `NoSlotAvailableException`, `ResourceNotFoundException`, `SlotAllocationException`, `UnauthorizedAccessException` |
| `flight_exceptions.py` | `DuplicateFlightNumberException`, `InvalidFlightDataException`, `InvalidFlightException` |
| `shared_exceptions.py` | `AuthenticationException`, `AuthenticationFailedException`, `AuthorizationException`, `ConcurrentModificationException`, `ResourceNotFoundException`, `UnauthorizedAccessException` |
| `slot_exceptions.py` | `NoAvailableSlotException`, `NoSlotAvailableException`, `SlotAllocationException` |

### `shared.value_objects` · layer: `domain`

Path: `src/domain/value_objects`
> Reusable value objects like FlightNumber, SlotTime, TimeInterval are needed across multiple domain packages to avoid duplication and ensure consistency.

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
| `test_flight_flow.py` | — |
| `test_slot_flow.py` | — |
| `test_runway_flow.py` | — |
| `test_emergency_flight_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #46 — Flight Registration System

**As a** air traffic controller
**I need** register incoming and outgoing flights with their details (flight number, type, scheduled time)
**So that** the system can track all aircraft movements

### Details and Assumptions
* The system must store flight number, aircraft type, and scheduled time for each flight.
* Both incoming and outgoing flights need to be registered separately.
* The registration process should validate that all required fields are provided.

### Acceptance Criteria

```gherkin
Given the system is ready to accept flight registrations
When the air traffic controller registers an incoming flight with flight number "AA123", type "Boeing 737", and scheduled time "14:30"
Then the system records the flight and it appears in the aircraft movement log
```

**UML class diagram:** `experiments/project_7/class_diagram_46.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/runway/runway_router.py` | `Actor` |
| `src/domain/exceptions/__init__.py` | `AuthorizationException`, `DuplicateFlightNumberException`, `InvalidFlightDataException` |
| `src/domain/exceptions/flight_exceptions.py` | `DuplicateFlightNumberException`, `InvalidFlightDataException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthorizationException` |
| `src/domain/flight/Flight.py` | `Actor`, `AircraftMovementLog`, `Direction`, `Flight`, `Interface`, `InterfaceKind`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Permission`, `Resource`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/dto/flight/flight_dto.py` | `FlightRegistrationRequest`, `FlightRegistrationResponse` |
| `src/repository/flight/flight_repository.py` | `AircraftMovementLogDatabase`, `FlightRegistrationAPI` |
| `src/repository/slot/slot_repository.py` | `Interface` |
| `src/service/flight/flight_service.py` | `FlightRegistrationService` |

---

### Task #47 — Slot Allocation Algorithm

**As a** air traffic controller
**I need** the system to automatically allocate the earliest available 5-minute time slot with a mandatory 3-minute gap between consecutive slots
**So that** safe separation between flights is ensured

### Details and Assumptions
* The system will manage a rolling schedule of time slots.
* A mandatory 3-minute gap must be enforced between the end of one slot and the start of the next.
* The "earliest available" slot is calculated based on current time or a given reference time.

### Acceptance Criteria

```gherkin
Given a schedule with existing allocated slots
When I request a new time slot allocation
Then the system assigns the earliest 5-minute slot that respects a 3-minute gap before and after any existing allocations
```

**UML class diagram:** `experiments/project_7/class_diagram_47.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/runway/runway_router.py` | `Actor` |
| `src/api/slot/slot_router.py` | `SlotAllocationController` |
| `src/domain/exceptions/__init__.py` | `AuthenticationException`, `AuthorizationException`, `NoAvailableSlotException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationException`, `AuthorizationException` |
| `src/domain/exceptions/slot_exceptions.py` | `NoAvailableSlotException` |
| `src/domain/flight/Flight.py` | `Actor`, `Interface`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Permission`, `Resource`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Operation`, `OperationSlot`, `Permission`, `Resource`, `Slot`, `State` |
| `src/dto/slot/slot_dto.py` | `SlotAllocationRequest`, `SlotAllocationResponse` |
| `src/repository/slot/slot_repository.py` | `Air_Traffic_Control_Console`, `Interface` |

---

### Task #48 — Arrival Priority Handling

**As a** air traffic controller  
**I need** arrival flights to be given priority over departure flights when allocating slots  
**So that** incoming aircraft can land safely and efficiently.  

### Details and Assumptions
* The system manages runway slots for both arriving and departing aircraft.  
* Priority is to be given to arrival flights over departure flights in slot allocation decisions.  
* The system must not compromise safety or create conflicts with other constraints (e.g., separation minima).  
* The assumption is that all flights have valid schedules and no other overriding priorities exist.  

### Acceptance Criteria

```gherkin
Given a set of arrival flights and departure flights competing for the same slot window
When the slot allocation process runs
Then all arrival flights are allocated slots before any departure flights are considered.

Given an arrival flight and a departure flight that both request the same slot time
When the conflict is resolved by the system
Then the arrival flight receives the slot.

Given a departure flight has already been allocated a slot
When an arrival flight requests that same slot
Then the system reallocates the slot to the arrival flight and reassigns the departure flight to the next available slot.
```

**UML class diagram:** `experiments/project_7/class_diagram_48.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/emergency_flight/EmergencyFlight.py` | `FlightType`, `SlotStatus` |
| `src/domain/exceptions/__init__.py` | `InvalidFlightException`, `SlotAllocationException` |
| `src/domain/exceptions/flight_exceptions.py` | `InvalidFlightException` |
| `src/domain/exceptions/slot_exceptions.py` | `SlotAllocationException` |
| `src/domain/flight/Flight.py` | `Flight`, `Permission` |
| `src/domain/runway/Runway.py` | `Permission`, `Runway` |
| `src/domain/slot/Slot.py` | `Permission`, `Slot` |
| `src/service/emergency_flight/emergency_flight_service.py` | `FlightScheduleDatabase` |

---

### Task #49 — Overlap Detection and Prevention

**As a** air traffic controller
**I need** the system to detect and prevent overlapping assignments where two flights would occupy the same slot or runway simultaneously
**So that** safe operations are ensured

### Details and Assumptions
* The system monitors all flight assignments for slot and runway usage.
* Overlaps are defined as two or more flights assigned to the same resource at the same time.
* The system should proactively prevent such overlaps from being created, not just detect them after the fact.

### Acceptance Criteria

```gherkin
Given a flight assignment is being created or modified
When the assignment would result in two flights occupying the same slot or runway at the same time
Then the system should reject the assignment and notify the air traffic controller of the conflict
```

**UML class diagram:** `experiments/project_7/class_diagram_49.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Permission`, `Resource`, `State` |
| `src/domain/slot/Slot.py` | `Permission`, `Resource`, `State` |

---

### Task #50 — Runway Closure Management

**As a** air traffic controller
**I need** the system to handle runway closures by automatically reassigning affected flights to alternative runways and marking them with appropriate delays
**So that** flights are safely and efficiently rerouted while maintaining separation rules

### Details and Assumptions
* The system has real-time knowledge of runway closures and available alternative runways.
* Flights scheduled to use the closed runway are identified automatically.
* Alternative runways have sufficient capacity and configuration for the aircraft types.
* Delay marking adjusts estimated departure/arrival times accordingly.
* Separation rules (e.g., wake turbulence, runway spacing) are enforced during reassignment.

### Acceptance Criteria

```gherkin
Given a runway closure has been declared for runway 27L
And flight A123 is scheduled to depart from runway 27L
When the system processes the runway closure
Then flight A123 is reassigned to an alternative runway (e.g., 27R)
And flight A123's departure time is updated with an appropriate delay
And separation rules between all affected flights are maintained

Given a runway closure for runway 27L
And multiple flights are affected (e.g., flight B456, C789)
When the system reassigns flights
Then each flight is assigned to a suitable alternative runway based on aircraft type and current traffic
And no two flights are assigned to the same runway within minimum separation time
```

**UML class diagram:** `experiments/project_7/class_diagram_50.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/runway/runway_router.py` | `AirTrafficControlTeam`, `FlightOperationsManagement`, `SafetyComplianceOffice` |
| `src/domain/flight/Flight.py` | `Flight`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Aircraft`, `Permission`, `PermissionLevel`, `PostState`, `PreState`, `Resource`, `Runway`, `RunwayStatus`, `SeparationRule`, `State`, `TrafficData`, `WakeTurbulenceCategory` |
| `src/domain/slot/Slot.py` | `Permission`, `Resource`, `Slot`, `State` |
| `src/repository/runway/runway_repository.py` | `AircraftAndTrafficDatabase`, `RunwayStatusAPI`, `SeparationRulesDatabase` |
| `src/service/runway/runway_service.py` | `System` |

---

### Task #51 — Emergency Flight Handling

**As a** air traffic controller  
**I need** the system to handle emergency flights by immediately allocating the next available slot and re-queuing all other affected flights to make room for the emergency  
**So that** ensuring rapid response to critical situations  

### Details and Assumptions  
* The system maintains a queue of scheduled flights with assigned slots.  
* Emergency flights are flagged and prioritized above all others.  
* Re-queuing affected flights may shift their departure/arrival times, but they remain in a consistent order.  
* The slot allocation for emergencies does not require manual confirmation—it happens automatically.  

### Acceptance Criteria  

```gherkin
Given an incoming emergency flight is detected  
When the system allocates the next available slot  
Then the emergency flight is inserted into that slot  
And all other previously queued flights are re-queued in order with adjusted slots  

Given a queue of non-emergency flights exists  
When an emergency flight is allocated a slot  
Then no non-emergency flight loses its original order  
And the emergency flight is placed at the front of the queue (in the next available slot)  
```

**UML class diagram:** `experiments/project_7/class_diagram_51.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/emergency_flight/emergency_flight_router.py` | `FlightQueueController` |
| `src/domain/emergency_flight/EmergencyFlight.py` | `EmergencyFlight`, `FlightQueue`, `FlightType`, `SlotStatus` |
| `src/domain/exceptions/__init__.py` | `AuthenticationFailedException`, `ConcurrentModificationException`, `NoSlotAvailableException`, `UnauthorizedAccessException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationFailedException`, `ConcurrentModificationException`, `UnauthorizedAccessException` |
| `src/domain/exceptions/slot_exceptions.py` | `NoSlotAvailableException` |
| `src/domain/flight/Flight.py` | `Flight` |
| `src/domain/slot/Slot.py` | `Slot` |
| `src/dto/emergency_flight/emergency_flight_dto.py` | `EmergencyRequestDTO`, `FlightDTO`, `QueueStatusDTO`, `SlotDTO` |
| `src/repository/emergency_flight/emergency_flight_repository.py` | `EmergencyHandler`, `QueueManager` |
| `src/service/emergency_flight/emergency_flight_service.py` | `FlightQueueAPI`, `FlightScheduleDatabase` |

---

### Task #52 — Runway Slot Timetable Display

**As a** air traffic controller
**I need** to view a slot timetable per runway showing all allocated time slots, flight details, and status
**So that** I can monitor and manage runway utilization at a glance.

### Details and Assumptions
* The timetable should display data organized per runway.
* It must include allocated time slots, flight details (e.g., flight number, aircraft type), and status (e.g., scheduled, landed, delayed).
* The view is intended for quick monitoring and decision support.

### Acceptance Criteria

```gherkin
Given I am an air traffic controller accessing the runway management system
When I select a specific runway to view its timetable
Then I should see a slot timetable showing allocated time slots, flight details, and status for that runway
```

**UML class diagram:** `experiments/project_7/class_diagram_52.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/emergency_flight/EmergencyFlight.py` | `SlotStatus` |
| `src/domain/exceptions/__init__.py` | `AuthenticationException`, `AuthorizationException`, `ResourceNotFoundException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationException`, `AuthorizationException`, `ResourceNotFoundException` |
| `src/domain/flight/Flight.py` | `Flight`, `Operation`, `Permission`, `State` |
| `src/domain/runway/Runway.py` | `Permission`, `Runway`, `State` |
| `src/domain/slot/Slot.py` | `Operation`, `Permission`, `Slot`, `State` |

---
