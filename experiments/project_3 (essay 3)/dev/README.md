# Project 10 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 31 |
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

### `domain.flight` · layer: `domain`

Path: `src/domain/flight`
> Domain layer for the Flight domain class

| File | Classes |
|------|---------|
| `Flight.py` | `Flight`, `Actor`, `Resource`, `Interface`, `Permission`, `State`, `IfaceKind`, `Operation`, `FlightId`, `FlightCreatedEvent`, `FlightUpdatedEvent` |

### `dto.flight` · layer: `dto`

Path: `src/dto/flight`
> Dto layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_dto.py` | `FlightCreateRequest`, `FlightUpdateRequest`, `FlightResponse` |

### `repository.flight` · layer: `repository`

Path: `src/repository/flight`
> Repository layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_repository.py` | `FlightRepository` |

### `orm.flight` · layer: `orm`

Path: `src/orm/flight`
> Orm layer for the Flight domain class

| File | Classes |
|------|---------|
| `flight_orm.py` | `FlightORM` |

### `events.flight` · layer: `infra`

Path: `src/infra/flight`
> domain events for flight registration, slot allocation, and runway closure to support event-driven CI/CD pipelines and logging

*(no files specified)*

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
| `flight_service.py` | `FlightService`, `FlightServiceImpl` |

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
| `Slot.py` | `Slot`, `Actor`, `Resource`, `Operation`, `Permission`, `State`, `SlotId`, `SlotCreatedEvent`, `SlotUpdatedEvent` |

### `dto.slot` · layer: `dto`

Path: `src/dto/slot`
> Dto layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_dto.py` | `SlotCreateRequest`, `SlotUpdateRequest`, `SlotResponse` |

### `repository.slot` · layer: `repository`

Path: `src/repository/slot`
> Repository layer for the Slot domain class

| File | Classes |
|------|---------|
| `slot_repository.py` | `SchedulingAPI`, `SchedulingDatabase` |

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
| `slot_router.py` | `SlotRouter` |

### `tests.unit.slot` · layer: `tests`

Path: `tests/unit/slot`
> Unit tests for Slot across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_slot_domain.py` | — |
| `test_slot_service.py` | — |
| `test_slot_api.py` | — |

### `domain.runway` · layer: `domain`

Path: `src/domain/runway`
> Domain layer for the Runway domain class

| File | Classes |
|------|---------|
| `Runway.py` | `Permission`, `Actor`, `Resource`, `State`, `Pre1`, `Pre2`, `Post1`, `Post2`, `Post3`, `RunwayClosureRequest`, `FlightSchedule`, `DelayCalculation`, `Airport_Operations_Manager`, `Flight_Control_Center`, `Passenger_Services_Department`, `Runway`, `RunwayId`, `RunwayCreatedEvent`, `RunwayUpdatedEvent` |

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
| `runway_repository.py` | `Interface`, `Runway_Closure_API`, `Flight_Schedule_Database`, `Airport_Operations_Manager_Console` |

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
| `runway_service.py` | `REQ_OPM_01` |

### `api.runway` · layer: `api`

Path: `src/api/runway`
> Api layer for the Runway domain class

| File | Classes |
|------|---------|
| `runway_router.py` | `RunwayRouter` |

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
> common domain exceptions (e.g., SlotOverlapException, RunwayClosureException) needed across all domain packages

| File | Classes |
|------|---------|
| `__init__.py` | `AmbiguousFlightClassificationException`, `ApiUnavailableException`, `AuthenticationException`, `AuthenticationFailedException`, `AuthenticationRequiredException`, `AuthorizationException`, `DatabaseException`, `DoubleBookingException`, `InsufficientPermissionException`, `InvalidStateTransitionException`, `NoScheduledSlotsException`, `ResourceNotAccessibleException`, `SlotOverlapException`, `SlotUnavailableException`, `UnauthorizedException`, `UnauthorizedOperationException` |
| `flight_exceptions.py` | `AmbiguousFlightClassificationException` |
| `shared_exceptions.py` | `ApiUnavailableException`, `AuthenticationException`, `AuthenticationFailedException`, `AuthenticationRequiredException`, `AuthorizationException`, `DatabaseException`, `DoubleBookingException`, `InsufficientPermissionException`, `InvalidStateTransitionException`, `ResourceNotAccessibleException`, `UnauthorizedException`, `UnauthorizedOperationException` |
| `slot_exceptions.py` | `NoScheduledSlotsException`, `SlotOverlapException`, `SlotUnavailableException` |

### `shared.utils` · layer: `infra`

Path: `src/infra/utils`
> time utilities for 5-minute slots, gap calculations, and date-time formatting required by multiple service layers

*(no files specified)*

### `config.di` · layer: `config`

Path: `src/config/di`
> dependency injection configuration to wire services, repositories, and orm across all modules for testability and deployment

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
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #72 — Flight Registration System

**As a** flight dispatcher
**I need** to register flights with estimated times
**So that** the airline can maintain accurate schedules and coordinate operations

### Details and Assumptions
* The system allows entry of flight number, origin, destination, and estimated departure/arrival times.
* Estimated times can be updated later if needed.
* Users have proper authorization to register flights.

### Acceptance Criteria

```gherkin
Given I am a logged-in flight dispatcher
When I enter a flight number, origin, destination, and estimated departure time
Then the flight is registered in the system with the provided estimated times
```

**UML class diagram:** `experiments/project_10/class_diagram_72.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Actor`, `Flight`, `IfaceKind`, `Interface`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/repository/runway/runway_repository.py` | `Interface` |

---

### Task #73 — Slot Allocation

**As a** scheduler
**I need** to allocate 5-minute slots with a 3-minute gap between successive slots
**So that** there is adequate buffer time between appointments

### Details and Assumptions
* Each slot duration is exactly 5 minutes
* A 3-minute gap is inserted after each slot before the next slot begins
* The gap is not part of the slot time

### Acceptance Criteria

```gherkin
Given a scheduling system
When I create a series of time slots
Then each slot is 5 minutes long
And there is a 3-minute gap between the end of one slot and the start of the next
```

**UML class diagram:** `experiments/project_10/class_diagram_73.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Actor`, `Operation`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Operation`, `Permission`, `Resource`, `Slot`, `State` |
| `src/repository/slot/slot_repository.py` | `SchedulingAPI`, `SchedulingDatabase` |

---

### Task #74 — Arrival Priority

**As a** airport slot coordinator
**I need** to prioritize arrivals over departures when allocating slots
**So that** landing aircraft receive preferential handling over departing ones

### Details and Assumptions
* Arrivals are considered higher priority than departures in slot allocation decisions
* This affects how slots are assigned when there are competing requests
* The system should enforce this priority during the allocation process

### Acceptance Criteria

```gherkin
Given multiple slot requests for the same time period
When the slot allocation is being processed
Then arrival slots are allocated before departure slots
```

**UML class diagram:** `experiments/project_10/class_diagram_74.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/exceptions/__init__.py` | `AuthenticationException`, `AuthorizationException`, `DoubleBookingException`, `InvalidStateTransitionException`, `SlotUnavailableException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationException`, `AuthorizationException`, `DoubleBookingException`, `InvalidStateTransitionException` |
| `src/domain/exceptions/slot_exceptions.py` | `SlotUnavailableException` |
| `src/domain/flight/Flight.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `State` |
| `src/domain/runway/Runway.py` | `Actor`, `Permission`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Permission`, `Slot`, `State` |
| `src/repository/runway/runway_repository.py` | `Interface` |

---

### Task #75 — Conflict Detection

**As a** scheduler
**I need** to detect and prevent slot overlaps and gap violations
**So that** resources are scheduled efficiently without conflicts or wasteful gaps

### Details and Assumptions
* Slots represent time intervals for resource allocation.
* Overlaps occur when two or more slots occupy the same time period.
* Gap violations occur when the distance between consecutive slots falls outside an acceptable range (e.g., too short or too long).
* The system should automatically check for conflicts during slot creation or modification.
* Prevention may include blocking the action or providing a warning with suggested alternatives.

### Acceptance Criteria

```gherkin
Given a schedule with existing slots
When a user attempts to create or modify a slot that overlaps with an existing slot
Then the system rejects the action and displays an error message indicating the overlap
```

**UML class diagram:** `experiments/project_10/class_diagram_75.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/exceptions/__init__.py` | `AuthenticationFailedException`, `SlotOverlapException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationFailedException` |
| `src/domain/exceptions/slot_exceptions.py` | `SlotOverlapException` |
| `src/domain/flight/Flight.py` | `Actor`, `Permission` |
| `src/domain/runway/Runway.py` | `Actor`, `Permission` |
| `src/domain/slot/Slot.py` | `Actor`, `Permission`, `Slot` |
| `src/dto/slot/slot_dto.py` | `SlotResponse` |

---

### Task #76 — Runway Closure Handling

**As a** airport operations manager
**I need** to close a runway and reassign flights, and mark flights as delayed if the delay exceeds 60 minutes
**So that** flights are safely and efficiently rerouted and accurate delay information is recorded

### Details and Assumptions
* The system manages runway assignments and flight schedules.
* Runway closure may be due to maintenance, weather, or emergency.
* Reassignment must consider available alternate runways and slots.
* Delay is calculated from original scheduled departure or arrival time.
* Flights with delay > 60 minutes are explicitly marked as delayed in the system.

### Acceptance Criteria

```gherkin
Given a runway is closed
When flights are reassigned to other runways
Then the system calculates the new delay for each flight
And if the delay exceeds 60 minutes, the flight is marked as delayed
```

**UML class diagram:** `experiments/project_10/class_diagram_76.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/flight/Flight.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/runway/Runway.py` | `Actor`, `Airport_Operations_Manager`, `DelayCalculation`, `FlightSchedule`, `Flight_Control_Center`, `Passenger_Services_Department`, `Permission`, `Post1`, `Post2`, `Post3`, `Pre2`, `Resource`, `RunwayClosureRequest`, `State` |
| `src/domain/slot/Slot.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/repository/runway/runway_repository.py` | `Airport_Operations_Manager_Console`, `Flight_Schedule_Database`, `Interface`, `Runway_Closure_API` |
| `src/service/runway/runway_service.py` | `REQ_OPM_01` |

---

### Task #77 — Emergency Flight Handling

**As a** air traffic controller
**I need** to assign an immediate slot to emergency flights and re-queue other flights
**So that** emergency flights are prioritized without disrupting overall scheduling

### Details and Assumptions
* The system must support dynamic slot reassignment.
* Re-queuing should maintain order for non-emergency flights.
* Emergency flights are identified by a flag or priority code.

### Acceptance Criteria

```gherkin
Given an emergency flight is detected
When the system assigns an immediate slot
Then the emergency flight is moved to the front of the queue
And all other flights are re-queued in their original order
```

**UML class diagram:** `experiments/project_10/class_diagram_77.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/exceptions/__init__.py` | `AmbiguousFlightClassificationException`, `AuthenticationRequiredException`, `InsufficientPermissionException`, `ResourceNotAccessibleException` |
| `src/domain/exceptions/flight_exceptions.py` | `AmbiguousFlightClassificationException` |
| `src/domain/exceptions/shared_exceptions.py` | `AuthenticationRequiredException`, `InsufficientPermissionException`, `ResourceNotAccessibleException` |
| `src/domain/flight/Flight.py` | `Actor`, `Flight`, `Permission` |
| `src/domain/runway/Runway.py` | `Actor`, `Permission` |
| `src/domain/slot/Slot.py` | `Actor`, `Permission`, `Slot` |

---

### Task #78 — Slot Timetable Display

**As a** air traffic controller
**I need** to view a slot timetable per runway that includes delays and emergency flights
**So that** I can manage runway scheduling efficiently and prioritize emergency operations

### Details and Assumptions
* The timetable should be filterable by runway.
* Delays are shown as updated departure/arrival times.
* Emergency flights are clearly marked (e.g., with a flag or color).
* The view is real-time or near real-time.

### Acceptance Criteria

```gherkin
Given I am on the runway slot timetable view
When I select a specific runway
Then I see a list of scheduled slots for that runway
And each slot shows the flight ID, scheduled time, and current status (on-time, delayed, or emergency)
```

**UML class diagram:** `experiments/project_10/class_diagram_78.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/exceptions/__init__.py` | `ApiUnavailableException`, `DatabaseException`, `NoScheduledSlotsException`, `UnauthorizedOperationException` |
| `src/domain/exceptions/shared_exceptions.py` | `ApiUnavailableException`, `DatabaseException`, `UnauthorizedOperationException` |
| `src/domain/exceptions/slot_exceptions.py` | `NoScheduledSlotsException` |
| `src/domain/flight/Flight.py` | `Flight`, `Permission` |
| `src/domain/runway/Runway.py` | `Permission`, `Runway` |
| `src/domain/slot/Slot.py` | `Permission`, `Slot` |

---
