# Project 13 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 75 |
| Requirements linked | 6 |
| Tasks | 6 |
| Domain classes | 9 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.account` · layer: `domain`

Path: `src/domain/account`
> Domain layer for the Account domain class

| File | Classes |
|------|---------|
| `Account.py` | `Permission`, `IfaceKind`, `Actor`, `Bank_Users`, `Customer_Support`, `IT_Team`, `State`, `Pre1`, `Pre2`, `Post1`, `Resource`, `Interface`, `Account_Balance_Database`, `Daily_Withdrawal_Tracking_Service`, `Account`, `AccountId`, `AccountCreatedEvent`, `AccountUpdatedEvent` |

### `dto.account` · layer: `dto`

Path: `src/dto/account`
> Dto layer for the Account domain class

| File | Classes |
|------|---------|
| `account_dto.py` | `AccountCreateRequest`, `AccountUpdateRequest`, `AccountResponse` |

### `repository.account` · layer: `repository`

Path: `src/repository/account`
> Repository layer for the Account domain class

| File | Classes |
|------|---------|
| `account_repository.py` | `AccountRepository` |

### `orm.account` · layer: `orm`

Path: `src/orm/account`
> Orm layer for the Account domain class

| File | Classes |
|------|---------|
| `account_orm.py` | `AccountORM` |

### `infra.account` · layer: `infra`

Path: `src/infra/account`
> Infra layer for the Account domain class

| File | Classes |
|------|---------|
| `account_repo_impl.py` | `SQLAlchemyAccountRepository` |

### `service.account` · layer: `service`

Path: `src/service/account`
> Service layer for the Account domain class

| File | Classes |
|------|---------|
| `account_service.py` | `REQ_BAL_01` |

### `api.account` · layer: `api`

Path: `src/api/account`
> Api layer for the Account domain class

| File | Classes |
|------|---------|
| `account_router.py` | `AccountRouter` |

### `tests.unit.account` · layer: `tests`

Path: `tests/unit/account`
> Unit tests for Account across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_account_domain.py` | — |
| `test_account_service.py` | — |
| `test_account_api.py` | — |

### `domain.authentication_attempt` · layer: `domain`

Path: `src/domain/authentication_attempt`
> Domain layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `AuthenticationAttempt.py` | `Permission`, `ActorRole`, `AuthenticationOutcome`, `Actor`, `SystemAdministrator`, `SecurityTeamMember`, `AuditEvent`, `AuthenticationAttempt`, `TransactionStateChange`, `AuditLogResource`, `AuthenticationAttemptId`, `AuthenticationAttemptCreatedEvent`, `AuthenticationAttemptUpdatedEvent` |

### `dto.authentication_attempt` · layer: `dto`

Path: `src/dto/authentication_attempt`
> Dto layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_dto.py` | `AuthenticationAttemptCreateRequest`, `AuthenticationAttemptUpdateRequest`, `AuthenticationAttemptResponse` |

### `repository.authentication_attempt` · layer: `repository`

Path: `src/repository/authentication_attempt`
> Repository layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_repository.py` | `AuthenticationAPI`, `AuditLogDatabase` |

### `orm.authentication_attempt` · layer: `orm`

Path: `src/orm/authentication_attempt`
> Orm layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_orm.py` | `AuthenticationAttemptORM` |

### `infra.authentication_attempt` · layer: `infra`

Path: `src/infra/authentication_attempt`
> Infra layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_repo_impl.py` | `SQLAlchemyAuthenticationAttemptRepository` |

### `service.authentication_attempt` · layer: `service`

Path: `src/service/authentication_attempt`
> Service layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_service.py` | `AuditService`, `AccessControlService` |

### `api.authentication_attempt` · layer: `api`

Path: `src/api/authentication_attempt`
> Api layer for the AuthenticationAttempt domain class

| File | Classes |
|------|---------|
| `authentication_attempt_router.py` | `AuthenticationAttemptRouter` |

### `tests.unit.authentication_attempt` · layer: `tests`

Path: `tests/unit/authentication_attempt`
> Unit tests for AuthenticationAttempt across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_authentication_attempt_domain.py` | — |
| `test_authentication_attempt_service.py` | — |
| `test_authentication_attempt_api.py` | — |

### `domain.card` · layer: `domain`

Path: `src/domain/card`
> Domain layer for the Card domain class

| File | Classes |
|------|---------|
| `Card.py` | `User`, `Card`, `AuthenticationSession`, `LockoutRecord`, `FailedAttempt`, `LockoutNotification`, `Permission`, `State`, `CardId`, `CardCreatedEvent`, `CardUpdatedEvent` |

### `dto.card` · layer: `dto`

Path: `src/dto/card`
> Dto layer for the Card domain class

| File | Classes |
|------|---------|
| `card_dto.py` | `AuthenticationRequestDTO`, `AuthenticationResponseDTO`, `LockoutStatusDTO` |

### `repository.card` · layer: `repository`

Path: `src/repository/card`
> Repository layer for the Card domain class

| File | Classes |
|------|---------|
| `card_repository.py` | `CardRepository` |

### `orm.card` · layer: `orm`

Path: `src/orm/card`
> Orm layer for the Card domain class

| File | Classes |
|------|---------|
| `card_orm.py` | `CardORM` |

### `infra.card` · layer: `infra`

Path: `src/infra/card`
> Infra layer for the Card domain class

| File | Classes |
|------|---------|
| `card_repo_impl.py` | `SQLAlchemyCardRepository` |

### `service.card` · layer: `service`

Path: `src/service/card`
> Service layer for the Card domain class

| File | Classes |
|------|---------|
| `card_service.py` | `CardService`, `CardServiceImpl` |

### `api.card` · layer: `api`

Path: `src/api/card`
> Api layer for the Card domain class

| File | Classes |
|------|---------|
| `card_router.py` | `AuthenticationController` |

### `tests.unit.card` · layer: `tests`

Path: `tests/unit/card`
> Unit tests for Card across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_card_domain.py` | — |
| `test_card_service.py` | — |
| `test_card_api.py` | — |

### `domain.daily_withdrawal_limit` · layer: `domain`

Path: `src/domain/daily_withdrawal_limit`
> Domain layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `DailyWithdrawalLimit.py` | `Permission`, `IfaceKind`, `Actor`, `Bank_Users`, `Customer_Support`, `IT_Team`, `State`, `Pre1`, `Pre2`, `Post1`, `Resource`, `Interface`, `Account_Balance_Database`, `Daily_Withdrawal_Tracking_Service`, `DailyWithdrawalLimit`, `DailyWithdrawalLimitId`, `DailyWithdrawalLimitCreatedEvent`, `DailyWithdrawalLimitUpdatedEvent` |

### `dto.daily_withdrawal_limit` · layer: `dto`

Path: `src/dto/daily_withdrawal_limit`
> Dto layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_dto.py` | `DailyWithdrawalLimitCreateRequest`, `DailyWithdrawalLimitUpdateRequest`, `DailyWithdrawalLimitResponse` |

### `repository.daily_withdrawal_limit` · layer: `repository`

Path: `src/repository/daily_withdrawal_limit`
> Repository layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_repository.py` | `DailyWithdrawalLimitRepository` |

### `orm.daily_withdrawal_limit` · layer: `orm`

Path: `src/orm/daily_withdrawal_limit`
> Orm layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_orm.py` | `DailyWithdrawalLimitORM` |

### `infra.daily_withdrawal_limit` · layer: `infra`

Path: `src/infra/daily_withdrawal_limit`
> Infra layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_repo_impl.py` | `SQLAlchemyDailyWithdrawalLimitRepository` |

### `service.daily_withdrawal_limit` · layer: `service`

Path: `src/service/daily_withdrawal_limit`
> Service layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_service.py` | `REQ_BAL_01` |

### `api.daily_withdrawal_limit` · layer: `api`

Path: `src/api/daily_withdrawal_limit`
> Api layer for the DailyWithdrawalLimit domain class

| File | Classes |
|------|---------|
| `daily_withdrawal_limit_router.py` | `DailyWithdrawalLimitRouter` |

### `tests.unit.daily_withdrawal_limit` · layer: `tests`

Path: `tests/unit/daily_withdrawal_limit`
> Unit tests for DailyWithdrawalLimit across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_daily_withdrawal_limit_domain.py` | — |
| `test_daily_withdrawal_limit_service.py` | — |
| `test_daily_withdrawal_limit_api.py` | — |

### `domain.pin` · layer: `domain`

Path: `src/domain/pin`
> Domain layer for the Pin domain class

| File | Classes |
|------|---------|
| `Pin.py` | `User`, `AuthenticationSession`, `LockoutRecord`, `FailedAttempt`, `LockoutNotification`, `Permission`, `State`, `Pin`, `PinId`, `PinCreatedEvent`, `PinUpdatedEvent` |

### `dto.pin` · layer: `dto`

Path: `src/dto/pin`
> Dto layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_dto.py` | `AuthenticationRequestDTO`, `AuthenticationResponseDTO`, `LockoutStatusDTO` |

### `repository.pin` · layer: `repository`

Path: `src/repository/pin`
> Repository layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_repository.py` | `PinRepository` |

### `orm.pin` · layer: `orm`

Path: `src/orm/pin`
> Orm layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_orm.py` | `PinORM` |

### `infra.pin` · layer: `infra`

Path: `src/infra/pin`
> Infra layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_repo_impl.py` | `SQLAlchemyPinRepository` |

### `service.pin` · layer: `service`

Path: `src/service/pin`
> Service layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_service.py` | `PinService`, `PinServiceImpl` |

### `api.pin` · layer: `api`

Path: `src/api/pin`
> Api layer for the Pin domain class

| File | Classes |
|------|---------|
| `pin_router.py` | `AuthenticationController` |

### `tests.unit.pin` · layer: `tests`

Path: `tests/unit/pin`
> Unit tests for Pin across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_pin_domain.py` | — |
| `test_pin_service.py` | — |
| `test_pin_api.py` | — |

### `domain.transaction_state` · layer: `domain`

Path: `src/domain/transaction_state`
> Domain layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `TransactionState.py` | `TransactionState`, `TransactionStateId`, `TransactionStateCreatedEvent`, `TransactionStateUpdatedEvent` |

### `dto.transaction_state` · layer: `dto`

Path: `src/dto/transaction_state`
> Dto layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_dto.py` | `TransactionStateCreateRequest`, `TransactionStateUpdateRequest`, `TransactionStateResponse` |

### `repository.transaction_state` · layer: `repository`

Path: `src/repository/transaction_state`
> Repository layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_repository.py` | `TransactionStateRepository` |

### `orm.transaction_state` · layer: `orm`

Path: `src/orm/transaction_state`
> Orm layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_orm.py` | `TransactionStateORM` |

### `infra.transaction_state` · layer: `infra`

Path: `src/infra/transaction_state`
> Infra layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_repo_impl.py` | `SQLAlchemyTransactionStateRepository` |

### `service.transaction_state` · layer: `service`

Path: `src/service/transaction_state`
> Service layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_service.py` | `TransactionStateService`, `TransactionStateServiceImpl` |

### `api.transaction_state` · layer: `api`

Path: `src/api/transaction_state`
> Api layer for the TransactionState domain class

| File | Classes |
|------|---------|
| `transaction_state_router.py` | `TransactionStateRouter` |

### `tests.unit.transaction_state` · layer: `tests`

Path: `tests/unit/transaction_state`
> Unit tests for TransactionState across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_transaction_state_domain.py` | — |
| `test_transaction_state_service.py` | — |
| `test_transaction_state_api.py` | — |

### `domain.withdrawal_transaction` · layer: `domain`

Path: `src/domain/withdrawal_transaction`
> Domain layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `WithdrawalTransaction.py` | `UserAccount`, `WithdrawalLimit`, `TransactionLog`, `WithdrawalRequest`, `AccountBalance`, `LoadAlert`, `StorageState`, `Actor`, `Permission`, `State`, `WithdrawalTransaction`, `WithdrawalTransactionId`, `WithdrawalTransactionCreatedEvent`, `WithdrawalTransactionUpdatedEvent` |

### `dto.withdrawal_transaction` · layer: `dto`

Path: `src/dto/withdrawal_transaction`
> Dto layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_dto.py` | `WithdrawalTransactionCreateRequest`, `WithdrawalTransactionUpdateRequest`, `WithdrawalTransactionResponse` |

### `repository.withdrawal_transaction` · layer: `repository`

Path: `src/repository/withdrawal_transaction`
> Repository layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_repository.py` | `AccountService_API`, `LimitService_API`, `TransactionLog_Database` |

### `orm.withdrawal_transaction` · layer: `orm`

Path: `src/orm/withdrawal_transaction`
> Orm layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_orm.py` | `WithdrawalTransactionORM` |

### `infra.withdrawal_transaction` · layer: `infra`

Path: `src/infra/withdrawal_transaction`
> Infra layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_repo_impl.py` | `SQLAlchemyWithdrawalTransactionRepository` |

### `service.withdrawal_transaction` · layer: `service`

Path: `src/service/withdrawal_transaction`
> Service layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_service.py` | `WithdrawalTransactionService`, `WithdrawalTransactionServiceImpl` |

### `api.withdrawal_transaction` · layer: `api`

Path: `src/api/withdrawal_transaction`
> Api layer for the WithdrawalTransaction domain class

| File | Classes |
|------|---------|
| `withdrawal_transaction_router.py` | `WithdrawalTransactionRouter` |

### `tests.unit.withdrawal_transaction` · layer: `tests`

Path: `tests/unit/withdrawal_transaction`
> Unit tests for WithdrawalTransaction across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_withdrawal_transaction_domain.py` | — |
| `test_withdrawal_transaction_service.py` | — |
| `test_withdrawal_transaction_api.py` | — |

### `domain.flagged_transaction` · layer: `domain`

Path: `src/domain/flagged_transaction`
> Domain layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `FlaggedTransaction.py` | `Actor`, `Security_Team`, `Finance_Team`, `Operations_Team`, `Resource`, `Interface`, `Withdrawal_API`, `Transaction_Database`, `REQ_SEC_01`, `Permission`, `State`, `IfaceKind`, `FlaggedTransaction`, `FlaggedTransactionId`, `FlaggedTransactionCreatedEvent`, `FlaggedTransactionUpdatedEvent` |

### `dto.flagged_transaction` · layer: `dto`

Path: `src/dto/flagged_transaction`
> Dto layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_dto.py` | `FlaggedTransactionCreateRequest`, `FlaggedTransactionUpdateRequest`, `FlaggedTransactionResponse` |

### `repository.flagged_transaction` · layer: `repository`

Path: `src/repository/flagged_transaction`
> Repository layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_repository.py` | `FlaggedTransactionRepository` |

### `orm.flagged_transaction` · layer: `orm`

Path: `src/orm/flagged_transaction`
> Orm layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_orm.py` | `FlaggedTransactionORM` |

### `infra.flagged_transaction` · layer: `infra`

Path: `src/infra/flagged_transaction`
> Infra layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_repo_impl.py` | `SQLAlchemyFlaggedTransactionRepository` |

### `service.flagged_transaction` · layer: `service`

Path: `src/service/flagged_transaction`
> Service layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_service.py` | `WithdrawalTransaction`, `Account`, `FlaggedTransaction`, `SuspiciousPattern`, `ReviewStatus`, `PatternType` |

### `api.flagged_transaction` · layer: `api`

Path: `src/api/flagged_transaction`
> Api layer for the FlaggedTransaction domain class

| File | Classes |
|------|---------|
| `flagged_transaction_router.py` | `FlaggedTransactionRouter` |

### `tests.unit.flagged_transaction` · layer: `tests`

Path: `tests/unit/flagged_transaction`
> Unit tests for FlaggedTransaction across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_flagged_transaction_domain.py` | — |
| `test_flagged_transaction_service.py` | — |
| `test_flagged_transaction_api.py` | — |

### `domain.suspicious_pattern` · layer: `domain`

Path: `src/domain/suspicious_pattern`
> Domain layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `SuspiciousPattern.py` | `SuspiciousPattern`, `SuspiciousPatternId`, `SuspiciousPatternCreatedEvent`, `SuspiciousPatternUpdatedEvent` |

### `dto.suspicious_pattern` · layer: `dto`

Path: `src/dto/suspicious_pattern`
> Dto layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_dto.py` | `SuspiciousPatternCreateRequest`, `SuspiciousPatternUpdateRequest`, `SuspiciousPatternResponse` |

### `repository.suspicious_pattern` · layer: `repository`

Path: `src/repository/suspicious_pattern`
> Repository layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_repository.py` | `SuspiciousPatternRepository` |

### `orm.suspicious_pattern` · layer: `orm`

Path: `src/orm/suspicious_pattern`
> Orm layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_orm.py` | `SuspiciousPatternORM` |

### `infra.suspicious_pattern` · layer: `infra`

Path: `src/infra/suspicious_pattern`
> Infra layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_repo_impl.py` | `SQLAlchemySuspiciousPatternRepository` |

### `service.suspicious_pattern` · layer: `service`

Path: `src/service/suspicious_pattern`
> Service layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_service.py` | `SuspiciousPatternService`, `SuspiciousPatternServiceImpl` |

### `api.suspicious_pattern` · layer: `api`

Path: `src/api/suspicious_pattern`
> Api layer for the SuspiciousPattern domain class

| File | Classes |
|------|---------|
| `suspicious_pattern_router.py` | `SuspiciousPatternRouter` |

### `tests.unit.suspicious_pattern` · layer: `tests`

Path: `tests/unit/suspicious_pattern`
> Unit tests for SuspiciousPattern across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_suspicious_pattern_domain.py` | — |
| `test_suspicious_pattern_service.py` | — |
| `test_suspicious_pattern_api.py` | — |

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
| `test_account_flow.py` | — |
| `test_daily_withdrawal_limit_flow.py` | — |
| `test_authentication_attempt_flow.py` | — |
| `test_transaction_state_flow.py` | — |
| `test_card_flow.py` | — |
| `test_pin_flow.py` | — |
| `test_withdrawal_transaction_flow.py` | — |
| `test_flagged_transaction_flow.py` | — |
| `test_suspicious_pattern_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #96 — Card and PIN Authentication

**As a** user
**I need** to authenticate using my card and PIN, and have my account locked after 3 consecutive failed attempts
**So that** my account is protected from unauthorized access

### Details and Assumptions
* Card and PIN are the required authentication methods.
* Locking occurs after 3 consecutive failed attempts.

### Acceptance Criteria

```gherkin
Given I have inserted my card
When I enter an incorrect PIN three consecutive times
Then my account is locked
```

**UML class diagram:** `experiments/project_13/class_diagram_96.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/card/card_router.py` | `AuthenticationController` |
| `src/api/pin/pin_router.py` | `AuthenticationController` |
| `src/domain/account/Account.py` | `Account`, `Permission`, `State` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `AuthenticationAttempt`, `Permission` |
| `src/domain/card/Card.py` | `AuthenticationSession`, `Card`, `FailedAttempt`, `LockoutNotification`, `LockoutRecord`, `Permission`, `State`, `User` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Permission`, `State` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `Permission`, `State` |
| `src/domain/pin/Pin.py` | `AuthenticationSession`, `FailedAttempt`, `LockoutNotification`, `LockoutRecord`, `Permission`, `State`, `User` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `Permission`, `State` |
| `src/dto/card/card_dto.py` | `AuthenticationRequestDTO`, `AuthenticationResponseDTO`, `LockoutStatusDTO` |
| `src/dto/pin/pin_dto.py` | `AuthenticationRequestDTO`, `AuthenticationResponseDTO`, `LockoutStatusDTO` |
| `src/service/flagged_transaction/flagged_transaction_service.py` | `Account` |

---

### Task #97 — Withdrawal Limit Enforcement

**As a** user
**I need** the system to decline withdrawals that exceed my account balance or daily withdrawal limit
**So that** I cannot withdraw more than I have available or exceed my daily limit

### Details and Assumptions
* The system must check both the current account balance and the cumulative daily withdrawal amount before approving a withdrawal.
* The daily withdrawal limit resets at a predefined time (e.g., midnight).
* If either the requested amount is greater than the balance or the total daily withdrawals (including the current request) would exceed the limit, the withdrawal is declined.

### Acceptance Criteria

```gherkin
Given I have an account with a balance of $100 and a daily withdrawal limit of $200
And I have already withdrawn $150 today
When I attempt to withdraw $100
Then the system should decline the withdrawal
And display a message that the amount exceeds my balance or daily limit
```

**UML class diagram:** `experiments/project_13/class_diagram_97.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account_Balance_Database`, `Bank_Users`, `Daily_Withdrawal_Tracking_Service`, `IT_Team`, `IfaceKind`, `Permission`, `Post1`, `Pre1`, `Pre2`, `Resource` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `Permission` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Account_Balance_Database`, `Bank_Users`, `Daily_Withdrawal_Tracking_Service`, `IT_Team`, `IfaceKind`, `Permission`, `Post1`, `Pre1`, `Pre2`, `Resource` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `IfaceKind`, `Permission`, `Resource` |
| `src/domain/pin/Pin.py` | `Permission` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `Permission` |
| `src/service/account/account_service.py` | `REQ_BAL_01` |
| `src/service/daily_withdrawal_limit/daily_withdrawal_limit_service.py` | `REQ_BAL_01` |

---

### Task #98 — Atomic Withdrawal with Rollback

**As a** user
**I need** withdrawal transactions to be atomic with full rollback if any part fails
**So that** data remains consistent and no partial changes occur

### Details and Assumptions
* Atomic transaction: either all steps (deducting balance, updating limits, logging) succeed or none do.
* Any failure in any step triggers a complete rollback to the pre-transaction state.

### Acceptance Criteria

```gherkin
Given the user has a sufficient balance for a withdrawal
When the user initiates a withdrawal transaction
And a step in the transaction (e.g., logging) fails
Then the entire transaction is rolled back
And the user's balance is unchanged
And the withdrawal limits are unchanged
And no transaction log is recorded
```

**UML class diagram:** `experiments/project_13/class_diagram_98.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Actor`, `Permission`, `State` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `Actor`, `Permission` |
| `src/domain/card/Card.py` | `Permission`, `State` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Actor`, `Permission`, `State` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `Actor`, `Permission`, `State` |
| `src/domain/pin/Pin.py` | `Permission`, `State` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `AccountBalance`, `Actor`, `LoadAlert`, `Permission`, `State`, `StorageState`, `TransactionLog`, `UserAccount`, `WithdrawalLimit`, `WithdrawalRequest` |
| `src/repository/withdrawal_transaction/withdrawal_transaction_repository.py` | `AccountService_API`, `TransactionLog_Database` |
| `src/service/flagged_transaction/flagged_transaction_service.py` | `Account` |

---

### Task #99 — Suspicious Withdrawal Detection

**As a** system
**I need** to detect suspicious withdrawal patterns (e.g., rapid successive withdrawals, unusual amounts)
**So that** they can be flagged for review

### Details and Assumptions
* This is for a secure settlement engine that validates credentials, enforces spending caps, and audits anomalous patterns.
* Detection is based on criteria like rapid successive withdrawals or unusual amounts.
* Flagged patterns will be subject to manual or automated review.

### Acceptance Criteria

```gherkin
Given a secure settlement engine for cash disbursements
When a withdrawal pattern involves rapid successive withdrawals or unusual amounts
Then the pattern is flagged for review
```

**UML class diagram:** `experiments/project_13/class_diagram_99.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `Actor`, `Permission` |
| `src/domain/card/Card.py` | `Permission`, `State` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `Actor`, `Finance_Team`, `FlaggedTransaction`, `IfaceKind`, `Interface`, `Operations_Team`, `Permission`, `REQ_SEC_01`, `Resource`, `Security_Team`, `State`, `Transaction_Database`, `Withdrawal_API` |
| `src/domain/pin/Pin.py` | `Permission`, `State` |
| `src/domain/suspicious_pattern/SuspiciousPattern.py` | `SuspiciousPattern` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `Actor`, `Permission`, `State`, `WithdrawalTransaction` |
| `src/service/flagged_transaction/flagged_transaction_service.py` | `Account`, `FlaggedTransaction`, `PatternType`, `ReviewStatus`, `SuspiciousPattern`, `WithdrawalTransaction` |

---

### Task #100 — Admin Transaction and Account Management

**As a** admin
**I need** to review flagged transactions, lock or unlock user accounts, and view transaction history for any user
**So that** I can manage user accounts and maintain security

### Details and Assumptions
* The admin has access to a dashboard or interface for managing users and transactions
* Flagged transactions are those identified as suspicious or requiring review
* Locking an account prevents further transactions, while unlocking restores access

### Acceptance Criteria

```gherkin
Given I am an authenticated admin
When I access the user management interface
Then I can view flagged transactions, lock or unlock accounts, and see transaction history for any user
```

**UML class diagram:** `experiments/project_13/class_diagram_100.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Account`, `Actor`, `State` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `Actor`, `TransactionStateChange` |
| `src/domain/card/Card.py` | `State`, `User` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Actor`, `State` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `Actor`, `FlaggedTransaction`, `State` |
| `src/domain/pin/Pin.py` | `State`, `User` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `Actor`, `State` |
| `src/service/flagged_transaction/flagged_transaction_service.py` | `Account`, `FlaggedTransaction` |

---

### Task #101 — Audit Logging for Authentication and Transactions

**As a** system administrator
**I need** to record all authentication attempts (successful/failed) and all transaction state changes with timestamps
**So that** I can audit system activity and ensure security compliance

### Details and Assumptions
* Both successful and failed login attempts must be logged
* All transaction state changes (e.g., pending, completed, failed) must be captured
* Each record must include a precise timestamp
* Logs should be stored in a tamper-proof or append-only format

### Acceptance Criteria

```gherkin
Given a user attempts to authenticate
When the authentication attempt completes (success or failure)
Then the system records the attempt with a timestamp and outcome

Given a transaction changes state
When the state transition occurs
Then the system records the new state with a timestamp
```

**UML class diagram:** `experiments/project_13/class_diagram_101.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/account/Account.py` | `Permission` |
| `src/domain/authentication_attempt/AuthenticationAttempt.py` | `ActorRole`, `AuditLogResource`, `AuthenticationAttempt`, `AuthenticationOutcome`, `Permission`, `SystemAdministrator`, `TransactionStateChange` |
| `src/domain/card/Card.py` | `Permission` |
| `src/domain/daily_withdrawal_limit/DailyWithdrawalLimit.py` | `Permission` |
| `src/domain/flagged_transaction/FlaggedTransaction.py` | `Permission` |
| `src/domain/pin/Pin.py` | `Permission` |
| `src/domain/transaction_state/TransactionState.py` | `TransactionState` |
| `src/domain/withdrawal_transaction/WithdrawalTransaction.py` | `Permission` |
| `src/repository/authentication_attempt/authentication_attempt_repository.py` | `AuthenticationAPI` |
| `src/service/authentication_attempt/authentication_attempt_service.py` | `AccessControlService`, `AuditService` |

---
