# Project 14 — Scaffold Reference

Auto-generated from the persisted package design, requirement artifacts, and UML diagrams.
Intended as a navigation aid for follow-up agents and developers.

---

## Statistics

| Item | Count |
|------|-------|
| Packages | 203 |
| Requirements linked | 12 |
| Tasks | 12 |
| Domain classes | 25 |

---

## Notes

- Generated files are implementation skeletons intended to be filled in by follow-up agents or developers.
- Existing files are preserved unless `overwrite_existing=True` is used.

---

## File Index

All generated files organised by package.

### `domain.badge` · layer: `domain`

Path: `src/domain/badge`
> Domain layer for the Badge domain class

| File | Classes |
|------|---------|
| `Badge.py` | `StudentAccount`, `RegistrationData`, `Avatar`, `Badge`, `BadgeId`, `BadgeCreatedEvent`, `BadgeUpdatedEvent` |

### `dto.badge` · layer: `dto`

Path: `src/dto/badge`
> Dto layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_dto.py` | `BadgeCreateRequest`, `BadgeUpdateRequest`, `BadgeResponse` |

### `repository.badge` · layer: `repository`

Path: `src/repository/badge`
> Repository layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_repository.py` | `BadgeRepository` |

### `orm.badge` · layer: `orm`

Path: `src/orm/badge`
> Orm layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_orm.py` | `BadgeORM` |

### `infra.badge` · layer: `infra`

Path: `src/infra/badge`
> Infra layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_repo_impl.py` | `SQLAlchemyBadgeRepository` |

### `service.badge` · layer: `service`

Path: `src/service/badge`
> Service layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_service.py` | `RegistrationService`, `RegistrationInput` |

### `api.badge` · layer: `api`

Path: `src/api/badge`
> Api layer for the Badge domain class

| File | Classes |
|------|---------|
| `badge_router.py` | `RegistrationController` |

### `tests.unit.badge` · layer: `tests`

Path: `tests/unit/badge`
> Unit tests for Badge across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_badge_domain.py` | — |
| `test_badge_service.py` | — |
| `test_badge_api.py` | — |

### `domain.competency` · layer: `domain`

Path: `src/domain/competency`
> Domain layer for the Competency domain class

| File | Classes |
|------|---------|
| `Competency.py` | `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `Competency`, `DifficultyTag`, `CompetencyId`, `CompetencyCreatedEvent`, `CompetencyUpdatedEvent` |

### `dto.competency` · layer: `dto`

Path: `src/dto/competency`
> Dto layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |

### `repository.competency` · layer: `repository`

Path: `src/repository/competency`
> Repository layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_repository.py` | `QuestionCreationAPI`, `ExamBuilderDatabase` |

### `orm.competency` · layer: `orm`

Path: `src/orm/competency`
> Orm layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_orm.py` | `CompetencyORM` |

### `infra.competency` · layer: `infra`

Path: `src/infra/competency`
> Infra layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_repo_impl.py` | `SQLAlchemyCompetencyRepository` |

### `service.competency` · layer: `service`

Path: `src/service/competency`
> Service layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_service.py` | `Operation` |

### `api.competency` · layer: `api`

Path: `src/api/competency`
> Api layer for the Competency domain class

| File | Classes |
|------|---------|
| `competency_router.py` | `CompetencyRouter` |

### `tests.unit.competency` · layer: `tests`

Path: `tests/unit/competency`
> Unit tests for Competency across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_competency_domain.py` | — |
| `test_competency_service.py` | — |
| `test_competency_api.py` | — |

### `domain.competency_breakdown` · layer: `domain`

Path: `src/domain/competency_breakdown`
> Domain layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `CompetencyBreakdown.py` | `Actor`, `Students`, `Academic_Advisors`, `Instructors`, `Resource`, `StudentDashboardResource`, `ExamAnalysisAPIResource`, `Permission`, `State`, `CompetencyBreakdown`, `CompetencyBreakdownId`, `CompetencyBreakdownCreatedEvent`, `CompetencyBreakdownUpdatedEvent` |

### `dto.competency_breakdown` · layer: `dto`

Path: `src/dto/competency_breakdown`
> Dto layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_dto.py` | `CompetencyBreakdownCreateRequest`, `CompetencyBreakdownUpdateRequest`, `CompetencyBreakdownResponse` |

### `repository.competency_breakdown` · layer: `repository`

Path: `src/repository/competency_breakdown`
> Repository layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_repository.py` | `Interface`, `Exam_Analysis_API`, `Student_Dashboard` |

### `orm.competency_breakdown` · layer: `orm`

Path: `src/orm/competency_breakdown`
> Orm layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_orm.py` | `CompetencyBreakdownORM` |

### `infra.competency_breakdown` · layer: `infra`

Path: `src/infra/competency_breakdown`
> Infra layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_repo_impl.py` | `SQLAlchemyCompetencyBreakdownRepository` |

### `service.competency_breakdown` · layer: `service`

Path: `src/service/competency_breakdown`
> Service layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_service.py` | `REQ_EDU_01` |

### `api.competency_breakdown` · layer: `api`

Path: `src/api/competency_breakdown`
> Api layer for the CompetencyBreakdown domain class

| File | Classes |
|------|---------|
| `competency_breakdown_router.py` | `CompetencyBreakdownRouter` |

### `tests.unit.competency_breakdown` · layer: `tests`

Path: `tests/unit/competency_breakdown`
> Unit tests for CompetencyBreakdown across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_competency_breakdown_domain.py` | — |
| `test_competency_breakdown_service.py` | — |
| `test_competency_breakdown_api.py` | — |

### `domain.exam_builder` · layer: `domain`

Path: `src/domain/exam_builder`
> Domain layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `ExamBuilder.py` | `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `DifficultyTag`, `ExamBuilder`, `ExamBuilderId`, `ExamBuilderCreatedEvent`, `ExamBuilderUpdatedEvent` |

### `dto.exam_builder` · layer: `dto`

Path: `src/dto/exam_builder`
> Dto layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |

### `repository.exam_builder` · layer: `repository`

Path: `src/repository/exam_builder`
> Repository layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_repository.py` | `QuestionCreationAPI`, `ExamBuilderDatabase` |

### `orm.exam_builder` · layer: `orm`

Path: `src/orm/exam_builder`
> Orm layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_orm.py` | `ExamBuilderORM` |

### `infra.exam_builder` · layer: `infra`

Path: `src/infra/exam_builder`
> Infra layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_repo_impl.py` | `SQLAlchemyExamBuilderRepository` |

### `service.exam_builder` · layer: `service`

Path: `src/service/exam_builder`
> Service layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_service.py` | `Operation` |

### `api.exam_builder` · layer: `api`

Path: `src/api/exam_builder`
> Api layer for the ExamBuilder domain class

| File | Classes |
|------|---------|
| `exam_builder_router.py` | `ExamBuilderRouter` |

### `tests.unit.exam_builder` · layer: `tests`

Path: `tests/unit/exam_builder`
> Unit tests for ExamBuilder across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_exam_builder_domain.py` | — |
| `test_exam_builder_service.py` | — |
| `test_exam_builder_api.py` | — |

### `domain.nugget_wallet` · layer: `domain`

Path: `src/domain/nugget_wallet`
> Domain layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `NuggetWallet.py` | `StudentAccount`, `RegistrationData`, `Avatar`, `NuggetWallet`, `NuggetWalletId`, `NuggetWalletCreatedEvent`, `NuggetWalletUpdatedEvent` |

### `dto.nugget_wallet` · layer: `dto`

Path: `src/dto/nugget_wallet`
> Dto layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_dto.py` | `NuggetWalletCreateRequest`, `NuggetWalletUpdateRequest`, `NuggetWalletResponse` |

### `repository.nugget_wallet` · layer: `repository`

Path: `src/repository/nugget_wallet`
> Repository layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_repository.py` | `NuggetWalletRepository` |

### `orm.nugget_wallet` · layer: `orm`

Path: `src/orm/nugget_wallet`
> Orm layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_orm.py` | `NuggetWalletORM` |

### `infra.nugget_wallet` · layer: `infra`

Path: `src/infra/nugget_wallet`
> Infra layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_repo_impl.py` | `SQLAlchemyNuggetWalletRepository` |

### `service.nugget_wallet` · layer: `service`

Path: `src/service/nugget_wallet`
> Service layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_service.py` | `RegistrationService`, `RegistrationInput` |

### `api.nugget_wallet` · layer: `api`

Path: `src/api/nugget_wallet`
> Api layer for the NuggetWallet domain class

| File | Classes |
|------|---------|
| `nugget_wallet_router.py` | `RegistrationController` |

### `tests.unit.nugget_wallet` · layer: `tests`

Path: `tests/unit/nugget_wallet`
> Unit tests for NuggetWallet across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_nugget_wallet_domain.py` | — |
| `test_nugget_wallet_service.py` | — |
| `test_nugget_wallet_api.py` | — |

### `domain.question` · layer: `domain`

Path: `src/domain/question`
> Domain layer for the Question domain class

| File | Classes |
|------|---------|
| `Question.py` | `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `DifficultyTag`, `Question`, `QuestionId`, `QuestionCreatedEvent`, `QuestionUpdatedEvent` |

### `dto.question` · layer: `dto`

Path: `src/dto/question`
> Dto layer for the Question domain class

| File | Classes |
|------|---------|
| `question_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |

### `repository.question` · layer: `repository`

Path: `src/repository/question`
> Repository layer for the Question domain class

| File | Classes |
|------|---------|
| `question_repository.py` | `QuestionCreationAPI`, `ExamBuilderDatabase` |

### `orm.question` · layer: `orm`

Path: `src/orm/question`
> Orm layer for the Question domain class

| File | Classes |
|------|---------|
| `question_orm.py` | `QuestionORM` |

### `infra.question` · layer: `infra`

Path: `src/infra/question`
> Infra layer for the Question domain class

| File | Classes |
|------|---------|
| `question_repo_impl.py` | `SQLAlchemyQuestionRepository` |

### `service.question` · layer: `service`

Path: `src/service/question`
> Service layer for the Question domain class

| File | Classes |
|------|---------|
| `question_service.py` | `Operation` |

### `api.question` · layer: `api`

Path: `src/api/question`
> Api layer for the Question domain class

| File | Classes |
|------|---------|
| `question_router.py` | `QuestionRouter` |

### `tests.unit.question` · layer: `tests`

Path: `tests/unit/question`
> Unit tests for Question across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_question_domain.py` | — |
| `test_question_service.py` | — |
| `test_question_api.py` | — |

### `domain.radar_chart` · layer: `domain`

Path: `src/domain/radar_chart`
> Domain layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `RadarChart.py` | `RadarChart`, `RadarChartId`, `RadarChartCreatedEvent`, `RadarChartUpdatedEvent` |

### `dto.radar_chart` · layer: `dto`

Path: `src/dto/radar_chart`
> Dto layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_dto.py` | `RadarChartCreateRequest`, `RadarChartUpdateRequest`, `RadarChartResponse` |

### `repository.radar_chart` · layer: `repository`

Path: `src/repository/radar_chart`
> Repository layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_repository.py` | `RadarChartRepository` |

### `orm.radar_chart` · layer: `orm`

Path: `src/orm/radar_chart`
> Orm layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_orm.py` | `RadarChartORM` |

### `infra.radar_chart` · layer: `infra`

Path: `src/infra/radar_chart`
> Infra layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_repo_impl.py` | `SQLAlchemyRadarChartRepository` |

### `service.radar_chart` · layer: `service`

Path: `src/service/radar_chart`
> Service layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_service.py` | `RadarChartService`, `RadarChartServiceImpl` |

### `api.radar_chart` · layer: `api`

Path: `src/api/radar_chart`
> Api layer for the RadarChart domain class

| File | Classes |
|------|---------|
| `radar_chart_router.py` | `RadarChartRouter` |

### `tests.unit.radar_chart` · layer: `tests`

Path: `tests/unit/radar_chart`
> Unit tests for RadarChart across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_radar_chart_domain.py` | — |
| `test_radar_chart_service.py` | — |
| `test_radar_chart_api.py` | — |

### `domain.schedule` · layer: `domain`

Path: `src/domain/schedule`
> Domain layer for the Schedule domain class

| File | Classes |
|------|---------|
| `Schedule.py` | `Schedule`, `ScheduleId`, `ScheduleCreatedEvent`, `ScheduleUpdatedEvent` |

### `dto.schedule` · layer: `dto`

Path: `src/dto/schedule`
> Dto layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_dto.py` | `ScheduleCreateRequest`, `ScheduleUpdateRequest`, `ScheduleResponse` |

### `repository.schedule` · layer: `repository`

Path: `src/repository/schedule`
> Repository layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_repository.py` | `ScheduleRepository` |

### `orm.schedule` · layer: `orm`

Path: `src/orm/schedule`
> Orm layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_orm.py` | `ScheduleORM` |

### `infra.schedule` · layer: `infra`

Path: `src/infra/schedule`
> Infra layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_repo_impl.py` | `SQLAlchemyScheduleRepository` |

### `service.schedule` · layer: `service`

Path: `src/service/schedule`
> Service layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_service.py` | `ScheduleService`, `ScheduleServiceImpl` |

### `api.schedule` · layer: `api`

Path: `src/api/schedule`
> Api layer for the Schedule domain class

| File | Classes |
|------|---------|
| `schedule_router.py` | `ScheduleRouter` |

### `tests.unit.schedule` · layer: `tests`

Path: `tests/unit/schedule`
> Unit tests for Schedule across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_schedule_domain.py` | — |
| `test_schedule_service.py` | — |
| `test_schedule_api.py` | — |

### `domain.student` · layer: `domain`

Path: `src/domain/student`
> Domain layer for the Student domain class

| File | Classes |
|------|---------|
| `Student.py` | `StudentAccount`, `RegistrationData`, `Avatar`, `Student`, `StudentId`, `StudentCreatedEvent`, `StudentUpdatedEvent` |

### `dto.student` · layer: `dto`

Path: `src/dto/student`
> Dto layer for the Student domain class

| File | Classes |
|------|---------|
| `student_dto.py` | `StudentCreateRequest`, `StudentUpdateRequest`, `StudentResponse` |

### `repository.student` · layer: `repository`

Path: `src/repository/student`
> Repository layer for the Student domain class

| File | Classes |
|------|---------|
| `student_repository.py` | `StudentRepository` |

### `orm.student` · layer: `orm`

Path: `src/orm/student`
> Orm layer for the Student domain class

| File | Classes |
|------|---------|
| `student_orm.py` | `StudentORM` |

### `infra.student` · layer: `infra`

Path: `src/infra/student`
> Infra layer for the Student domain class

| File | Classes |
|------|---------|
| `student_repo_impl.py` | `SQLAlchemyStudentRepository` |

### `service.student` · layer: `service`

Path: `src/service/student`
> Service layer for the Student domain class

| File | Classes |
|------|---------|
| `student_service.py` | `RegistrationService`, `RegistrationInput` |

### `api.student` · layer: `api`

Path: `src/api/student`
> Api layer for the Student domain class

| File | Classes |
|------|---------|
| `student_router.py` | `RegistrationController` |

### `tests.unit.student` · layer: `tests`

Path: `tests/unit/student`
> Unit tests for Student across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_student_domain.py` | — |
| `test_student_service.py` | — |
| `test_student_api.py` | — |

### `domain.attempt_review` · layer: `domain`

Path: `src/domain/attempt_review`
> Domain layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `AttemptReview.py` | `Attempt`, `ChartPoint`, `AttemptReview`, `AttemptReviewId`, `AttemptReviewCreatedEvent`, `AttemptReviewUpdatedEvent` |

### `dto.attempt_review` · layer: `dto`

Path: `src/dto/attempt_review`
> Dto layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_dto.py` | `AttemptReviewCreateRequest`, `AttemptReviewUpdateRequest`, `AttemptReviewResponse` |

### `repository.attempt_review` · layer: `repository`

Path: `src/repository/attempt_review`
> Repository layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_repository.py` | `StudentDashboardUI`, `StudentDataAPI`, `TrendAPI`, `StudentDataStore` |

### `orm.attempt_review` · layer: `orm`

Path: `src/orm/attempt_review`
> Orm layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_orm.py` | `AttemptReviewORM` |

### `infra.attempt_review` · layer: `infra`

Path: `src/infra/attempt_review`
> Infra layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_repo_impl.py` | `SQLAlchemyAttemptReviewRepository` |

### `service.attempt_review` · layer: `service`

Path: `src/service/attempt_review`
> Service layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_service.py` | `PastAttemptData`, `DashboardData`, `TrendData`, `ReviewService`, `AccessControlService`, `Permission`, `Role` |

### `api.attempt_review` · layer: `api`

Path: `src/api/attempt_review`
> Api layer for the AttemptReview domain class

| File | Classes |
|------|---------|
| `attempt_review_router.py` | `ReviewController` |

### `tests.unit.attempt_review` · layer: `tests`

Path: `tests/unit/attempt_review`
> Unit tests for AttemptReview across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_attempt_review_domain.py` | — |
| `test_attempt_review_service.py` | — |
| `test_attempt_review_api.py` | — |

### `domain.cohort` · layer: `domain`

Path: `src/domain/cohort`
> Domain layer for the Cohort domain class

| File | Classes |
|------|---------|
| `Cohort.py` | `Cohort`, `Exam`, `Administrator`, `IT_Team`, `CohortId`, `CohortCreatedEvent`, `CohortUpdatedEvent` |

### `dto.cohort` · layer: `dto`

Path: `src/dto/cohort`
> Dto layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_dto.py` | `CohortCreateRequest`, `CohortUpdateRequest`, `CohortResponse` |

### `repository.cohort` · layer: `repository`

Path: `src/repository/cohort`
> Repository layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_repository.py` | `CohortRepository` |

### `orm.cohort` · layer: `orm`

Path: `src/orm/cohort`
> Orm layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_orm.py` | `CohortORM` |

### `infra.cohort` · layer: `infra`

Path: `src/infra/cohort`
> Infra layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_repo_impl.py` | `SQLAlchemyCohortRepository` |

### `service.cohort` · layer: `service`

Path: `src/service/cohort`
> Service layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_service.py` | `CohortService`, `CohortServiceImpl` |

### `api.cohort` · layer: `api`

Path: `src/api/cohort`
> Api layer for the Cohort domain class

| File | Classes |
|------|---------|
| `cohort_router.py` | `CohortRouter` |

### `tests.unit.cohort` · layer: `tests`

Path: `tests/unit/cohort`
> Unit tests for Cohort across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_cohort_domain.py` | — |
| `test_cohort_service.py` | — |
| `test_cohort_api.py` | — |

### `domain.cohort_leaderboard` · layer: `domain`

Path: `src/domain/cohort_leaderboard`
> Domain layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `CohortLeaderboard.py` | `Actor`, `Resource`, `Interface`, `Permission`, `State`, `CohortLeaderboard`, `CohortLeaderboardId`, `CohortLeaderboardCreatedEvent`, `CohortLeaderboardUpdatedEvent` |

### `dto.cohort_leaderboard` · layer: `dto`

Path: `src/dto/cohort_leaderboard`
> Dto layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_dto.py` | `CohortLeaderboardCreateRequest`, `CohortLeaderboardUpdateRequest`, `CohortLeaderboardResponse` |

### `repository.cohort_leaderboard` · layer: `repository`

Path: `src/repository/cohort_leaderboard`
> Repository layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_repository.py` | `Student_Data_Store`, `Cohort_Settings_API`, `Leaderboard_Display` |

### `orm.cohort_leaderboard` · layer: `orm`

Path: `src/orm/cohort_leaderboard`
> Orm layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_orm.py` | `CohortLeaderboardORM` |

### `infra.cohort_leaderboard` · layer: `infra`

Path: `src/infra/cohort_leaderboard`
> Infra layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_repo_impl.py` | `SQLAlchemyCohortLeaderboardRepository` |

### `service.cohort_leaderboard` · layer: `service`

Path: `src/service/cohort_leaderboard`
> Service layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_service.py` | `REQ_COHORT_LEADERBOARD_01` |

### `api.cohort_leaderboard` · layer: `api`

Path: `src/api/cohort_leaderboard`
> Api layer for the CohortLeaderboard domain class

| File | Classes |
|------|---------|
| `cohort_leaderboard_router.py` | `CohortLeaderboardRouter` |

### `tests.unit.cohort_leaderboard` · layer: `tests`

Path: `tests/unit/cohort_leaderboard`
> Unit tests for CohortLeaderboard across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_cohort_leaderboard_domain.py` | — |
| `test_cohort_leaderboard_service.py` | — |
| `test_cohort_leaderboard_api.py` | — |

### `domain.competency_trend_chart` · layer: `domain`

Path: `src/domain/competency_trend_chart`
> Domain layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `CompetencyTrendChart.py` | `Attempt`, `ChartPoint`, `CompetencyTrendChart`, `CompetencyTrendChartId`, `CompetencyTrendChartCreatedEvent`, `CompetencyTrendChartUpdatedEvent` |

### `dto.competency_trend_chart` · layer: `dto`

Path: `src/dto/competency_trend_chart`
> Dto layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_dto.py` | `CompetencyTrendChartCreateRequest`, `CompetencyTrendChartUpdateRequest`, `CompetencyTrendChartResponse` |

### `repository.competency_trend_chart` · layer: `repository`

Path: `src/repository/competency_trend_chart`
> Repository layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_repository.py` | `StudentDashboardUI`, `StudentDataAPI`, `TrendAPI`, `StudentDataStore` |

### `orm.competency_trend_chart` · layer: `orm`

Path: `src/orm/competency_trend_chart`
> Orm layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_orm.py` | `CompetencyTrendChartORM` |

### `infra.competency_trend_chart` · layer: `infra`

Path: `src/infra/competency_trend_chart`
> Infra layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_repo_impl.py` | `SQLAlchemyCompetencyTrendChartRepository` |

### `service.competency_trend_chart` · layer: `service`

Path: `src/service/competency_trend_chart`
> Service layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_service.py` | `PastAttemptData`, `DashboardData`, `TrendData`, `ReviewService`, `AccessControlService`, `Permission`, `Role` |

### `api.competency_trend_chart` · layer: `api`

Path: `src/api/competency_trend_chart`
> Api layer for the CompetencyTrendChart domain class

| File | Classes |
|------|---------|
| `competency_trend_chart_router.py` | `ReviewController` |

### `tests.unit.competency_trend_chart` · layer: `tests`

Path: `tests/unit/competency_trend_chart`
> Unit tests for CompetencyTrendChart across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_competency_trend_chart_domain.py` | — |
| `test_competency_trend_chart_service.py` | — |
| `test_competency_trend_chart_api.py` | — |

### `domain.enrollment` · layer: `domain`

Path: `src/domain/enrollment`
> Domain layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `Enrollment.py` | `Exam`, `Administrator`, `IT_Team`, `Enrollment`, `EnrollmentId`, `EnrollmentCreatedEvent`, `EnrollmentUpdatedEvent` |

### `dto.enrollment` · layer: `dto`

Path: `src/dto/enrollment`
> Dto layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_dto.py` | `EnrollmentCreateRequest`, `EnrollmentUpdateRequest`, `EnrollmentResponse` |

### `repository.enrollment` · layer: `repository`

Path: `src/repository/enrollment`
> Repository layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_repository.py` | `EnrollmentRepository` |

### `orm.enrollment` · layer: `orm`

Path: `src/orm/enrollment`
> Orm layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_orm.py` | `EnrollmentORM` |

### `infra.enrollment` · layer: `infra`

Path: `src/infra/enrollment`
> Infra layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_repo_impl.py` | `SQLAlchemyEnrollmentRepository` |

### `service.enrollment` · layer: `service`

Path: `src/service/enrollment`
> Service layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_service.py` | `EnrollmentService`, `EnrollmentServiceImpl` |

### `api.enrollment` · layer: `api`

Path: `src/api/enrollment`
> Api layer for the Enrollment domain class

| File | Classes |
|------|---------|
| `enrollment_router.py` | `EnrollmentRouter` |

### `tests.unit.enrollment` · layer: `tests`

Path: `tests/unit/enrollment`
> Unit tests for Enrollment across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_enrollment_domain.py` | — |
| `test_enrollment_service.py` | — |
| `test_enrollment_api.py` | — |

### `domain.exam_session` · layer: `domain`

Path: `src/domain/exam_session`
> Domain layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `ExamSession.py` | `IT_Team`, `Exam`, `ExamSession`, `ExamStatus`, `Permission`, `ExamSessionId`, `ExamSessionCreatedEvent`, `ExamSessionUpdatedEvent` |

### `dto.exam_session` · layer: `dto`

Path: `src/dto/exam_session`
> Dto layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_dto.py` | `ExamSessionCreateRequest`, `ExamSessionUpdateRequest`, `ExamSessionResponse` |

### `repository.exam_session` · layer: `repository`

Path: `src/repository/exam_session`
> Repository layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_repository.py` | `ExamSessionRepository` |

### `orm.exam_session` · layer: `orm`

Path: `src/orm/exam_session`
> Orm layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_orm.py` | `ExamSessionORM` |

### `infra.exam_session` · layer: `infra`

Path: `src/infra/exam_session`
> Infra layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_repo_impl.py` | `SQLAlchemyExamSessionRepository` |

### `service.exam_session` · layer: `service`

Path: `src/service/exam_session`
> Service layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_service.py` | `ExamSessionService`, `ExamSessionServiceImpl` |

### `api.exam_session` · layer: `api`

Path: `src/api/exam_session`
> Api layer for the ExamSession domain class

| File | Classes |
|------|---------|
| `exam_session_router.py` | `ExamSessionRouter` |

### `tests.unit.exam_session` · layer: `tests`

Path: `tests/unit/exam_session`
> Unit tests for ExamSession across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_exam_session_domain.py` | — |
| `test_exam_session_service.py` | — |
| `test_exam_session_api.py` | — |

### `domain.instructor` · layer: `domain`

Path: `src/domain/instructor`
> Domain layer for the Instructor domain class

| File | Classes |
|------|---------|
| `Instructor.py` | `Actor`, `Instructor`, `InstructorAccount`, `DashboardContent`, `Exam`, `Permission`, `InstructorId`, `InstructorCreatedEvent`, `InstructorUpdatedEvent` |

### `dto.instructor` · layer: `dto`

Path: `src/dto/instructor`
> Dto layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_dto.py` | `InstructorCreateRequest`, `InstructorUpdateRequest`, `InstructorResponse` |

### `repository.instructor` · layer: `repository`

Path: `src/repository/instructor`
> Repository layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_repository.py` | `Registration_API`, `Login_API`, `User_Database`, `Dashboard_UI` |

### `orm.instructor` · layer: `orm`

Path: `src/orm/instructor`
> Orm layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_orm.py` | `InstructorORM` |

### `infra.instructor` · layer: `infra`

Path: `src/infra/instructor`
> Infra layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_repo_impl.py` | `SQLAlchemyInstructorRepository` |

### `service.instructor` · layer: `service`

Path: `src/service/instructor`
> Service layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_service.py` | `InstructorService`, `InstructorServiceImpl` |

### `api.instructor` · layer: `api`

Path: `src/api/instructor`
> Api layer for the Instructor domain class

| File | Classes |
|------|---------|
| `instructor_router.py` | `InstructorRouter` |

### `tests.unit.instructor` · layer: `tests`

Path: `tests/unit/instructor`
> Unit tests for Instructor across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_instructor_domain.py` | — |
| `test_instructor_service.py` | — |
| `test_instructor_api.py` | — |

### `domain.audit_event` · layer: `domain`

Path: `src/domain/audit_event`
> Domain layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `AuditEvent.py` | `Permission`, `State`, `Teacher`, `IT_Team`, `BonusNugget`, `Justification`, `AuditEvent`, `AuditEventId`, `AuditEventCreatedEvent`, `AuditEventUpdatedEvent` |

### `dto.audit_event` · layer: `dto`

Path: `src/dto/audit_event`
> Dto layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_dto.py` | `AuditEventCreateRequest`, `AuditEventUpdateRequest`, `AuditEventResponse` |

### `repository.audit_event` · layer: `repository`

Path: `src/repository/audit_event`
> Repository layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_repository.py` | `AuditEventRepository` |

### `orm.audit_event` · layer: `orm`

Path: `src/orm/audit_event`
> Orm layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_orm.py` | `AuditEventORM` |

### `infra.audit_event` · layer: `infra`

Path: `src/infra/audit_event`
> Infra layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_repo_impl.py` | `SQLAlchemyAuditEventRepository` |

### `service.audit_event` · layer: `service`

Path: `src/service/audit_event`
> Service layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_service.py` | `AuditEventService`, `AuditEventServiceImpl` |

### `api.audit_event` · layer: `api`

Path: `src/api/audit_event`
> Api layer for the AuditEvent domain class

| File | Classes |
|------|---------|
| `audit_event_router.py` | `AuditEventRouter` |

### `tests.unit.audit_event` · layer: `tests`

Path: `tests/unit/audit_event`
> Unit tests for AuditEvent across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_audit_event_domain.py` | — |
| `test_audit_event_service.py` | — |
| `test_audit_event_api.py` | — |

### `domain.bonu_nugget_grant` · layer: `domain`

Path: `src/domain/bonu_nugget_grant`
> Domain layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `BonuNuggetGrant.py` | `Permission`, `State`, `Teacher`, `IT_Team`, `BonusNugget`, `Justification`, `BonuNuggetGrant`, `BonuNuggetGrantId`, `BonuNuggetGrantCreatedEvent`, `BonuNuggetGrantUpdatedEvent` |

### `dto.bonu_nugget_grant` · layer: `dto`

Path: `src/dto/bonu_nugget_grant`
> Dto layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_dto.py` | `BonuNuggetGrantCreateRequest`, `BonuNuggetGrantUpdateRequest`, `BonuNuggetGrantResponse` |

### `repository.bonu_nugget_grant` · layer: `repository`

Path: `src/repository/bonu_nugget_grant`
> Repository layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_repository.py` | `BonuNuggetGrantRepository` |

### `orm.bonu_nugget_grant` · layer: `orm`

Path: `src/orm/bonu_nugget_grant`
> Orm layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_orm.py` | `BonuNuggetGrantORM` |

### `infra.bonu_nugget_grant` · layer: `infra`

Path: `src/infra/bonu_nugget_grant`
> Infra layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_repo_impl.py` | `SQLAlchemyBonuNuggetGrantRepository` |

### `service.bonu_nugget_grant` · layer: `service`

Path: `src/service/bonu_nugget_grant`
> Service layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_service.py` | `BonuNuggetGrantService`, `BonuNuggetGrantServiceImpl` |

### `api.bonu_nugget_grant` · layer: `api`

Path: `src/api/bonu_nugget_grant`
> Api layer for the BonuNuggetGrant domain class

| File | Classes |
|------|---------|
| `bonu_nugget_grant_router.py` | `BonuNuggetGrantRouter` |

### `tests.unit.bonu_nugget_grant` · layer: `tests`

Path: `tests/unit/bonu_nugget_grant`
> Unit tests for BonuNuggetGrant across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_bonu_nugget_grant_domain.py` | — |
| `test_bonu_nugget_grant_service.py` | — |
| `test_bonu_nugget_grant_api.py` | — |

### `domain.instructor_dashboard` · layer: `domain`

Path: `src/domain/instructor_dashboard`
> Domain layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `InstructorDashboard.py` | `Actor`, `InstructorAccount`, `DashboardContent`, `Exam`, `Permission`, `InstructorDashboard`, `InstructorDashboardId`, `InstructorDashboardCreatedEvent`, `InstructorDashboardUpdatedEvent` |

### `dto.instructor_dashboard` · layer: `dto`

Path: `src/dto/instructor_dashboard`
> Dto layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_dto.py` | `InstructorDashboardCreateRequest`, `InstructorDashboardUpdateRequest`, `InstructorDashboardResponse` |

### `repository.instructor_dashboard` · layer: `repository`

Path: `src/repository/instructor_dashboard`
> Repository layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_repository.py` | `Registration_API`, `Login_API`, `User_Database`, `Dashboard_UI` |

### `orm.instructor_dashboard` · layer: `orm`

Path: `src/orm/instructor_dashboard`
> Orm layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_orm.py` | `InstructorDashboardORM` |

### `infra.instructor_dashboard` · layer: `infra`

Path: `src/infra/instructor_dashboard`
> Infra layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_repo_impl.py` | `SQLAlchemyInstructorDashboardRepository` |

### `service.instructor_dashboard` · layer: `service`

Path: `src/service/instructor_dashboard`
> Service layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_service.py` | `InstructorDashboardService`, `InstructorDashboardServiceImpl` |

### `api.instructor_dashboard` · layer: `api`

Path: `src/api/instructor_dashboard`
> Api layer for the InstructorDashboard domain class

| File | Classes |
|------|---------|
| `instructor_dashboard_router.py` | `InstructorDashboardRouter` |

### `tests.unit.instructor_dashboard` · layer: `tests`

Path: `tests/unit/instructor_dashboard`
> Unit tests for InstructorDashboard across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_instructor_dashboard_domain.py` | — |
| `test_instructor_dashboard_service.py` | — |
| `test_instructor_dashboard_api.py` | — |

### `domain.redemption` · layer: `domain`

Path: `src/domain/redemption`
> Domain layer for the Redemption domain class

| File | Classes |
|------|---------|
| `Redemption.py` | `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `Redemption`, `RedemptionId`, `RedemptionCreatedEvent`, `RedemptionUpdatedEvent` |

### `dto.redemption` · layer: `dto`

Path: `src/dto/redemption`
> Dto layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_dto.py` | `RedemptionCreateRequest`, `RedemptionUpdateRequest`, `RedemptionResponse` |

### `repository.redemption` · layer: `repository`

Path: `src/repository/redemption`
> Repository layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_repository.py` | `RedemptionRepository` |

### `orm.redemption` · layer: `orm`

Path: `src/orm/redemption`
> Orm layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_orm.py` | `RedemptionORM` |

### `infra.redemption` · layer: `infra`

Path: `src/infra/redemption`
> Infra layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_repo_impl.py` | `SQLAlchemyRedemptionRepository` |

### `service.redemption` · layer: `service`

Path: `src/service/redemption`
> Service layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_service.py` | `REQ_STU_01` |

### `api.redemption` · layer: `api`

Path: `src/api/redemption`
> Api layer for the Redemption domain class

| File | Classes |
|------|---------|
| `redemption_router.py` | `RedemptionRouter` |

### `tests.unit.redemption` · layer: `tests`

Path: `tests/unit/redemption`
> Unit tests for Redemption across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_redemption_domain.py` | — |
| `test_redemption_service.py` | — |
| `test_redemption_api.py` | — |

### `domain.reward_item` · layer: `domain`

Path: `src/domain/reward_item`
> Domain layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `RewardItem.py` | `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `RewardItem`, `RewardItemId`, `RewardItemCreatedEvent`, `RewardItemUpdatedEvent` |

### `dto.reward_item` · layer: `dto`

Path: `src/dto/reward_item`
> Dto layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_dto.py` | `RewardItemCreateRequest`, `RewardItemUpdateRequest`, `RewardItemResponse` |

### `repository.reward_item` · layer: `repository`

Path: `src/repository/reward_item`
> Repository layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_repository.py` | `RewardItemRepository` |

### `orm.reward_item` · layer: `orm`

Path: `src/orm/reward_item`
> Orm layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_orm.py` | `RewardItemORM` |

### `infra.reward_item` · layer: `infra`

Path: `src/infra/reward_item`
> Infra layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_repo_impl.py` | `SQLAlchemyRewardItemRepository` |

### `service.reward_item` · layer: `service`

Path: `src/service/reward_item`
> Service layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_service.py` | `REQ_STU_01` |

### `api.reward_item` · layer: `api`

Path: `src/api/reward_item`
> Api layer for the RewardItem domain class

| File | Classes |
|------|---------|
| `reward_item_router.py` | `RewardItemRouter` |

### `tests.unit.reward_item` · layer: `tests`

Path: `tests/unit/reward_item`
> Unit tests for RewardItem across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_reward_item_domain.py` | — |
| `test_reward_item_service.py` | — |
| `test_reward_item_api.py` | — |

### `domain.reward_store` · layer: `domain`

Path: `src/domain/reward_store`
> Domain layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `RewardStore.py` | `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `RewardStore`, `RewardStoreId`, `RewardStoreCreatedEvent`, `RewardStoreUpdatedEvent` |

### `dto.reward_store` · layer: `dto`

Path: `src/dto/reward_store`
> Dto layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_dto.py` | `RewardStoreCreateRequest`, `RewardStoreUpdateRequest`, `RewardStoreResponse` |

### `repository.reward_store` · layer: `repository`

Path: `src/repository/reward_store`
> Repository layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_repository.py` | `RewardStoreRepository` |

### `orm.reward_store` · layer: `orm`

Path: `src/orm/reward_store`
> Orm layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_orm.py` | `RewardStoreORM` |

### `infra.reward_store` · layer: `infra`

Path: `src/infra/reward_store`
> Infra layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_repo_impl.py` | `SQLAlchemyRewardStoreRepository` |

### `service.reward_store` · layer: `service`

Path: `src/service/reward_store`
> Service layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_service.py` | `REQ_STU_01` |

### `api.reward_store` · layer: `api`

Path: `src/api/reward_store`
> Api layer for the RewardStore domain class

| File | Classes |
|------|---------|
| `reward_store_router.py` | `RewardStoreRouter` |

### `tests.unit.reward_store` · layer: `tests`

Path: `tests/unit/reward_store`
> Unit tests for RewardStore across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_reward_store_domain.py` | — |
| `test_reward_store_service.py` | — |
| `test_reward_store_api.py` | — |

### `domain.streak` · layer: `domain`

Path: `src/domain/streak`
> Domain layer for the Streak domain class

| File | Classes |
|------|---------|
| `Streak.py` | `Player`, `Streak`, `StreakId`, `StreakCreatedEvent`, `StreakUpdatedEvent` |

### `dto.streak` · layer: `dto`

Path: `src/dto/streak`
> Dto layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_dto.py` | `StreakCreateRequest`, `StreakUpdateRequest`, `StreakResponse` |

### `repository.streak` · layer: `repository`

Path: `src/repository/streak`
> Repository layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_repository.py` | `Actor`, `Resource`, `Interface`, `Permission`, `State`, `IfaceKind` |

### `orm.streak` · layer: `orm`

Path: `src/orm/streak`
> Orm layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_orm.py` | `StreakORM` |

### `infra.streak` · layer: `infra`

Path: `src/infra/streak`
> Infra layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_repo_impl.py` | `SQLAlchemyStreakRepository` |

### `service.streak` · layer: `service`

Path: `src/service/streak`
> Service layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_service.py` | `Operation` |

### `api.streak` · layer: `api`

Path: `src/api/streak`
> Api layer for the Streak domain class

| File | Classes |
|------|---------|
| `streak_router.py` | `StreakRouter` |

### `tests.unit.streak` · layer: `tests`

Path: `tests/unit/streak`
> Unit tests for Streak across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_streak_domain.py` | — |
| `test_streak_service.py` | — |
| `test_streak_api.py` | — |

### `domain.student_profile` · layer: `domain`

Path: `src/domain/student_profile`
> Domain layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `StudentProfile.py` | `StudentAccount`, `StudentProfile`, `RegistrationData`, `Avatar`, `StudentProfileId`, `StudentProfileCreatedEvent`, `StudentProfileUpdatedEvent` |

### `dto.student_profile` · layer: `dto`

Path: `src/dto/student_profile`
> Dto layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_dto.py` | `StudentProfileCreateRequest`, `StudentProfileUpdateRequest`, `StudentProfileResponse` |

### `repository.student_profile` · layer: `repository`

Path: `src/repository/student_profile`
> Repository layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_repository.py` | `StudentProfileRepository` |

### `orm.student_profile` · layer: `orm`

Path: `src/orm/student_profile`
> Orm layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_orm.py` | `StudentProfileORM` |

### `infra.student_profile` · layer: `infra`

Path: `src/infra/student_profile`
> Infra layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_repo_impl.py` | `SQLAlchemyStudentProfileRepository` |

### `service.student_profile` · layer: `service`

Path: `src/service/student_profile`
> Service layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_service.py` | `RegistrationService`, `RegistrationInput` |

### `api.student_profile` · layer: `api`

Path: `src/api/student_profile`
> Api layer for the StudentProfile domain class

| File | Classes |
|------|---------|
| `student_profile_router.py` | `RegistrationController` |

### `tests.unit.student_profile` · layer: `tests`

Path: `tests/unit/student_profile`
> Unit tests for StudentProfile across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_student_profile_domain.py` | — |
| `test_student_profile_service.py` | — |
| `test_student_profile_api.py` | — |

### `domain.study_tip` · layer: `domain`

Path: `src/domain/study_tip`
> Domain layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `StudyTip.py` | `Actor`, `Students`, `Academic_Advisors`, `Instructors`, `Resource`, `StudentDashboardResource`, `ExamAnalysisAPIResource`, `Permission`, `State`, `StudyTip`, `StudyTipId`, `StudyTipCreatedEvent`, `StudyTipUpdatedEvent` |

### `dto.study_tip` · layer: `dto`

Path: `src/dto/study_tip`
> Dto layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_dto.py` | `StudyTipCreateRequest`, `StudyTipUpdateRequest`, `StudyTipResponse` |

### `repository.study_tip` · layer: `repository`

Path: `src/repository/study_tip`
> Repository layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_repository.py` | `Interface`, `Exam_Analysis_API`, `Student_Dashboard` |

### `orm.study_tip` · layer: `orm`

Path: `src/orm/study_tip`
> Orm layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_orm.py` | `StudyTipORM` |

### `infra.study_tip` · layer: `infra`

Path: `src/infra/study_tip`
> Infra layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_repo_impl.py` | `SQLAlchemyStudyTipRepository` |

### `service.study_tip` · layer: `service`

Path: `src/service/study_tip`
> Service layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_service.py` | `REQ_EDU_01` |

### `api.study_tip` · layer: `api`

Path: `src/api/study_tip`
> Api layer for the StudyTip domain class

| File | Classes |
|------|---------|
| `study_tip_router.py` | `StudyTipRouter` |

### `tests.unit.study_tip` · layer: `tests`

Path: `tests/unit/study_tip`
> Unit tests for StudyTip across domain, service, and API layers

| File | Classes |
|------|---------|
| `test_study_tip_domain.py` | — |
| `test_study_tip_service.py` | — |
| `test_study_tip_api.py` | — |

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
| `test_exam_builder_flow.py` | — |
| `test_question_flow.py` | — |
| `test_competency_flow.py` | — |
| `test_schedule_flow.py` | — |
| `test_student_flow.py` | — |
| `test_student_profile_flow.py` | — |
| `test_nugget_wallet_flow.py` | — |
| `test_badge_flow.py` | — |
| `test_radar_chart_flow.py` | — |
| `test_competency_breakdown_flow.py` | — |
| `test_study_tip_flow.py` | — |
| `test_cohort_flow.py` | — |
| `test_enrollment_flow.py` | — |
| `test_attempt_review_flow.py` | — |
| `test_competency_trend_chart_flow.py` | — |
| `test_exam_session_flow.py` | — |
| `test_streak_flow.py` | — |
| `test_reward_store_flow.py` | — |
| `test_reward_item_flow.py` | — |
| `test_redemption_flow.py` | — |
| `test_cohort_leaderboard_flow.py` | — |
| `test_instructor_flow.py` | — |
| `test_instructor_dashboard_flow.py` | — |
| `test_bonu_nugget_grant_flow.py` | — |
| `test_audit_event_flow.py` | — |
| `test_api_contracts.py` | — |
| `conftest.py` | — |

---

## Task Index

For each task: full description, files whose classes appear in the task's UML diagram,
and paths to the linked requirement specification and UML diagrams.

### Task #105 — Instructor Registration, Login, and Dashboard

**As a** instructor  
**I need** to register and log in to a personal dashboard that shows active exams, enrollment counts, and competency coverage  
**So that** I can manage my courses and monitor student progress efficiently  

### Details and Assumptions
* The system must support instructor account creation and authentication.
* The dashboard is personalized per instructor.
* Active exams refer to exams that are currently ongoing or scheduled.
* Enrollment counts show the number of students enrolled in the instructor's courses.
* Competency coverage indicates which skills or topics are being assessed.

### Acceptance Criteria

```gherkin
Given an instructor is not registered
When they access the registration page
Then they can create an account with required details

Given an instructor has registered
When they log in with valid credentials
Then they are redirected to their personal dashboard

Given an instructor is on their dashboard
When they view the dashboard
Then they see active exams, enrollment counts, and competency coverage
```

**UML class diagram:** `experiments/project_14/class_diagram_105.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/cohort/Cohort.py` | `Exam` |
| `src/domain/competency/Competency.py` | `Competency` |
| `src/domain/enrollment/Enrollment.py` | `Exam` |
| `src/domain/exam_session/ExamSession.py` | `Exam` |
| `src/domain/instructor/Instructor.py` | `DashboardContent`, `Exam`, `Instructor` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `DashboardContent`, `Exam` |
| `src/repository/instructor/instructor_repository.py` | `Registration_API`, `User_Database` |
| `src/repository/instructor_dashboard/instructor_dashboard_repository.py` | `Registration_API`, `User_Database` |

---

### Task #106 — Exam Builder with Mixed Question Types

**As a** instructor
**I need** an exam builder that supports multiple choice, drag-and-drop, and code snippet questions, each tagged with one or more competencies and difficulty tiers (Beginner, Intermediate, Advanced), and associated nugget reward multipliers
**So that** I can create assessments that accurately test competencies with appropriate difficulty and reward learning

### Details and Assumptions
* The exam builder must allow creation of three question types: multiple choice, drag-and-drop, and code snippet.
* Each question can be tagged with multiple competencies and one difficulty tier.
* Difficulty tiers are Beginner, Intermediate, Advanced.
* Each question can have an associated nugget reward multiplier.

### Acceptance Criteria

```gherkin
Given I am an exam creator
When I create a new question of type multiple choice, drag-and-drop, or code snippet
Then I can assign one or more competencies, a difficulty tier from Beginner, Intermediate, or Advanced, and a nugget reward multiplier to that question
```

**UML class diagram:** `experiments/project_14/class_diagram_106.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `Permission`, `State` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission`, `State` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission`, `Resource`, `State` |
| `src/domain/competency/Competency.py` | `Competency`, `DifficultyTag`, `DifficultyTier`, `Permission`, `QuestionType`, `Resource`, `State` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Permission`, `Resource`, `State` |
| `src/domain/exam_builder/ExamBuilder.py` | `DifficultyTag`, `DifficultyTier`, `Permission`, `QuestionType`, `Resource`, `State` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Permission` |
| `src/domain/question/Question.py` | `DifficultyTag`, `DifficultyTier`, `Permission`, `Question`, `QuestionType`, `Resource`, `State` |
| `src/domain/redemption/Redemption.py` | `Resource` |
| `src/domain/reward_item/RewardItem.py` | `Resource` |
| `src/domain/reward_store/RewardStore.py` | `Resource` |
| `src/domain/study_tip/StudyTip.py` | `Permission`, `Resource`, `State` |
| `src/dto/competency/competency_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |
| `src/dto/exam_builder/exam_builder_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |
| `src/dto/question/question_dto.py` | `CreateQuestionRequest`, `CreateQuestionResponse` |
| `src/repository/competency/competency_repository.py` | `ExamBuilderDatabase`, `QuestionCreationAPI` |
| `src/repository/exam_builder/exam_builder_repository.py` | `ExamBuilderDatabase`, `QuestionCreationAPI` |
| `src/repository/question/question_repository.py` | `ExamBuilderDatabase`, `QuestionCreationAPI` |
| `src/repository/streak/streak_repository.py` | `Permission`, `Resource`, `State` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/competency/competency_service.py` | `Operation` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |
| `src/service/exam_builder/exam_builder_service.py` | `Operation` |
| `src/service/question/question_service.py` | `Operation` |
| `src/service/streak/streak_service.py` | `Operation` |

---

### Task #107 — Exam Scheduling

**As a** instructor
**I need** to schedule exams with an open date, close date, and optional per-attempt time limit enforced server-side
**So that** students can only access the exam within the specified time window and are limited to the allowed time per attempt

### Details and Assumptions
* The open and close dates define the period during which the exam is available to students.
* The per-attempt time limit is optional and, if set, is enforced on the server to prevent client-side manipulation.
* Students may have multiple attempts; the time limit applies to each attempt individually.
* The enforcement ensures that once the time limit expires, the attempt is automatically submitted.

### Acceptance Criteria

```gherkin
Given an exam is scheduled with an open date and a close date
When a student tries to access the exam outside that time window
Then the exam is not accessible and an appropriate message is displayed

Given an exam is scheduled with a per-attempt time limit of 60 minutes
When a student starts an attempt
Then the server records the start time and begins counting down the 60-minute limit
And when the time limit expires, the attempt is automatically submitted

Given an exam is scheduled with no per-attempt time limit
When a student starts an attempt
Then the student can take as much time as needed within the open/close window
```

**UML class diagram:** `experiments/project_14/class_diagram_107.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Instructors` |
| `src/domain/redemption/Redemption.py` | `IfaceKind` |
| `src/domain/reward_item/RewardItem.py` | `IfaceKind` |
| `src/domain/reward_store/RewardStore.py` | `IfaceKind` |
| `src/domain/study_tip/StudyTip.py` | `Instructors` |
| `src/repository/streak/streak_repository.py` | `IfaceKind` |

---

### Task #108 — Cohort Creation and Student Enrollment

**As a** administrator
**I need** to create cohorts, enroll individual students, and restrict exams to one or more cohorts
**So that** I can manage student groups and control exam access efficiently

### Details and Assumptions
* Cohorts are groups of students.
* Individual student enrollment allows adding students to specific cohorts.
* Exam restriction limits which cohorts can access a given exam.

### Acceptance Criteria

```gherkin
Given I am an administrator
When I create a new cohort
Then the cohort is saved and available for enrollment

Given I have a cohort
When I enroll an individual student
Then the student is added to that cohort

Given I have an exam and one or more cohorts
When I restrict the exam to those cohorts
Then only students in those cohorts can access the exam
```

**UML class diagram:** `experiments/project_14/class_diagram_108.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/cohort/Cohort.py` | `Administrator`, `Cohort`, `Exam` |
| `src/domain/enrollment/Enrollment.py` | `Administrator`, `Exam` |
| `src/domain/exam_session/ExamSession.py` | `Exam` |
| `src/domain/instructor/Instructor.py` | `Exam` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Exam` |
| `src/domain/student/Student.py` | `Student` |
| `src/service/cohort/cohort_service.py` | `CohortServiceImpl` |

---

### Task #109 — Manual Bonus Nuggets Grant

**As a** teacher
**I need** to grant manual bonus nuggets to individual students with a written justification
**So that** the justification is logged as an audit event for record-keeping

### Details and Assumptions
* Bonus nuggets are manually awarded to individual students.
* Each bonus grant must include a written justification.
* The system logs each bonus grant as an audit event with the justification.

### Acceptance Criteria

```gherkin
Given a teacher is logged into the system
When the teacher grants a manual bonus nugget to a student with a written justification
Then the bonus nugget is added to the student's account
And an audit event is created containing the teacher, student, amount, and justification
```

**UML class diagram:** `experiments/project_14/class_diagram_109.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `AuditEvent`, `BonusNugget`, `IT_Team`, `Justification`, `Permission`, `State`, `Teacher` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `BonusNugget`, `IT_Team`, `Justification`, `Permission`, `State`, `Teacher` |
| `src/domain/cohort/Cohort.py` | `IT_Team` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission`, `State` |
| `src/domain/competency/Competency.py` | `Permission`, `State` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Permission`, `State` |
| `src/domain/enrollment/Enrollment.py` | `IT_Team` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission`, `State` |
| `src/domain/exam_session/ExamSession.py` | `IT_Team`, `Permission` |
| `src/domain/instructor/Instructor.py` | `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Permission` |
| `src/domain/nugget_wallet/NuggetWallet.py` | `NuggetWallet` |
| `src/domain/question/Question.py` | `Permission`, `State` |
| `src/domain/student/Student.py` | `Student` |
| `src/domain/study_tip/StudyTip.py` | `Permission`, `State` |
| `src/repository/streak/streak_repository.py` | `Permission`, `State` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |

---

### Task #110 — Student Registration and Profile

**As a** Student  
**I need** to register and have a personalized profile including an avatar, nugget balance, earned badges, and a competency radar chart  
**So that** I can track my progress and have a customized learning experience  

### Details and Assumptions
* The registration process collects necessary user information and creates a profile.
* The profile automatically initializes with a default avatar, zero nugget balance, no earned badges, and an empty radar chart.
* Avatar can be customized during or after registration.
* Nugget balance, badges, and radar chart update based on platform activities.

### Acceptance Criteria

```gherkin
Given a new user wants to register
When they complete the registration form and submit
Then a student account is created
And a personalized profile is generated with a default avatar, zero nuggets, no badges, and an empty competency radar chart

Given a registered student navigates to their profile
When the profile page loads
Then they see their avatar, current nugget balance, earned badges, and competency radar chart
```

**UML class diagram:** `experiments/project_14/class_diagram_110.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/badge/badge_router.py` | `RegistrationController` |
| `src/api/nugget_wallet/nugget_wallet_router.py` | `RegistrationController` |
| `src/api/student/student_router.py` | `RegistrationController` |
| `src/api/student_profile/student_profile_router.py` | `RegistrationController` |
| `src/domain/audit_event/AuditEvent.py` | `Permission` |
| `src/domain/badge/Badge.py` | `Avatar`, `Badge`, `RegistrationData`, `StudentAccount` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission` |
| `src/domain/competency/Competency.py` | `Permission` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Permission` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Permission` |
| `src/domain/nugget_wallet/NuggetWallet.py` | `Avatar`, `RegistrationData`, `StudentAccount` |
| `src/domain/question/Question.py` | `Permission` |
| `src/domain/radar_chart/RadarChart.py` | `RadarChart` |
| `src/domain/student/Student.py` | `Avatar`, `RegistrationData`, `StudentAccount` |
| `src/domain/student_profile/StudentProfile.py` | `Avatar`, `RegistrationData`, `StudentAccount`, `StudentProfile` |
| `src/domain/study_tip/StudyTip.py` | `Permission` |
| `src/repository/streak/streak_repository.py` | `Permission` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/badge/badge_service.py` | `RegistrationInput`, `RegistrationService` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |
| `src/service/nugget_wallet/nugget_wallet_service.py` | `RegistrationInput`, `RegistrationService` |
| `src/service/student/student_service.py` | `RegistrationInput`, `RegistrationService` |
| `src/service/student_profile/student_profile_service.py` | `RegistrationInput`, `RegistrationService` |

---

### Task #111 — One-Question-at-a-Time Exam Delivery

**As a** student  
**I need** to have exams delivered one question at a time with a game-like interface, live timer, progress bar, and animated nugget counter  
**So that** I can stay engaged, track my progress, and feel motivated throughout the exam.

### Details and Assumptions
* The exam is presented in a single-question-per-screen format.
* The game-like interface includes visual elements and animations.
* The live timer counts down or up as appropriate.
* The progress bar shows completion percentage or question count.
* Animated nugget counter rewards correct answers or milestones.

### Acceptance Criteria

```gherkin
Given I am taking an exam
When I start the exam
Then I see one question at a time with a game-like interface, a live timer, a progress bar, and an animated nugget counter

Given I am on a question
When I answer and submit
Then the next question appears automatically and the progress bar updates

Given the timer reaches zero
When time expires
Then the current answer is submitted and the exam ends

Given I earn a nugget
When the counter updates
Then the nugget counter plays an animation
```

**UML class diagram:** `experiments/project_14/class_diagram_111.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `IT_Team`, `Permission` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `IT_Team`, `Permission` |
| `src/domain/cohort/Cohort.py` | `Exam`, `IT_Team` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission` |
| `src/domain/competency/Competency.py` | `Permission` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Permission` |
| `src/domain/enrollment/Enrollment.py` | `Exam`, `IT_Team` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission` |
| `src/domain/exam_session/ExamSession.py` | `Exam`, `ExamSession`, `ExamStatus`, `IT_Team`, `Permission` |
| `src/domain/instructor/Instructor.py` | `Exam`, `Instructor`, `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Exam`, `Permission` |
| `src/domain/nugget_wallet/NuggetWallet.py` | `NuggetWallet` |
| `src/domain/question/Question.py` | `Permission`, `Question` |
| `src/domain/student/Student.py` | `Student` |
| `src/domain/study_tip/StudyTip.py` | `Permission` |
| `src/repository/streak/streak_repository.py` | `Permission` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |

---

### Task #112 — Streak System with Nugget Multiplier

**As a** player
**I need** a streak system where consecutive correct answers apply a nugget multiplier (1.5×, 2×, 3×) that resets on a wrong answer
**So that** I can earn increased nuggets for maintaining a streak

### Details and Assumptions
* Nuggets are the in-game currency.
* The multiplier starts at 1× and increases to 1.5×, 2×, then 3× for consecutive correct answers.
* The multiplier resets to 1× after any wrong answer.
* The multiplier is applied to the base nugget reward for each correct answer.

### Acceptance Criteria

```gherkin
Given I am answering a question
When I answer correctly for the first time
Then I receive base nuggets (no multiplier)

Given I have answered correctly once
When I answer correctly again
Then I receive nuggets multiplied by 1.5×

Given I have answered correctly twice consecutively
When I answer correctly a third time
Then I receive nuggets multiplied by 2×

Given I have answered correctly three times consecutively
When I answer correctly a fourth time
Then I receive nuggets multiplied by 3×

Given I have a streak of at least one correct answer
When I answer incorrectly
Then my streak resets and the multiplier returns to 1×
```

**UML class diagram:** `experiments/project_14/class_diagram_112.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `Permission`, `State` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission`, `State` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/competency/Competency.py` | `Permission`, `Resource`, `State` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission`, `Resource`, `State` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Actor`, `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Actor`, `Permission` |
| `src/domain/nugget_wallet/NuggetWallet.py` | `NuggetWallet` |
| `src/domain/question/Question.py` | `Permission`, `Question`, `Resource`, `State` |
| `src/domain/redemption/Redemption.py` | `Actor`, `IfaceKind`, `Interface`, `Resource` |
| `src/domain/reward_item/RewardItem.py` | `Actor`, `IfaceKind`, `Interface`, `Resource` |
| `src/domain/reward_store/RewardStore.py` | `Actor`, `IfaceKind`, `Interface`, `Resource` |
| `src/domain/streak/Streak.py` | `Player`, `Streak` |
| `src/domain/study_tip/StudyTip.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/repository/competency_breakdown/competency_breakdown_repository.py` | `Interface` |
| `src/repository/streak/streak_repository.py` | `Actor`, `IfaceKind`, `Interface`, `Permission`, `Resource`, `State` |
| `src/repository/study_tip/study_tip_repository.py` | `Interface` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/competency/competency_service.py` | `Operation` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |
| `src/service/exam_builder/exam_builder_service.py` | `Operation` |
| `src/service/question/question_service.py` | `Operation` |
| `src/service/streak/streak_service.py` | `Operation` |

---

### Task #113 — Instant Competency Breakdown

**As a** student  
**I need** an instant competency breakdown after exam submission  
**So that** I can identify weak areas and get targeted study tips  

### Details and Assumptions
* The system analyzes exam results immediately after submission.
* Weak competency flags indicate areas needing improvement.
* Study tips are generated based on flagged weaknesses.

### Acceptance Criteria

```gherkin
Given I have submitted an exam
When the system processes my results
Then I see a competency breakdown with weak competency flags and study tips
```

**UML class diagram:** `experiments/project_14/class_diagram_113.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `Permission`, `State` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission`, `State` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission`, `State` |
| `src/domain/competency/Competency.py` | `Permission`, `State` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Instructors`, `Permission`, `State`, `StudentDashboardResource`, `Students` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission`, `State` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Permission` |
| `src/domain/question/Question.py` | `Permission`, `State` |
| `src/domain/study_tip/StudyTip.py` | `Instructors`, `Permission`, `State`, `StudentDashboardResource`, `Students` |
| `src/repository/competency_breakdown/competency_breakdown_repository.py` | `Exam_Analysis_API` |
| `src/repository/streak/streak_repository.py` | `Permission`, `State` |
| `src/repository/study_tip/study_tip_repository.py` | `Exam_Analysis_API` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/competency_breakdown/competency_breakdown_service.py` | `REQ_EDU_01` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |
| `src/service/study_tip/study_tip_service.py` | `REQ_EDU_01` |

---

### Task #114 — Student Nugget Wallet and Reward Store

**As a** student  
**I need** a nugget wallet redeemable in a reward store for virtual items or instructor-configured institutional perks  
**So that** I can spend my earned nuggets on meaningful rewards  

### Details and Assumptions
* Nuggets are earned through desired behaviors or achievements.
* The reward store contains both virtual items (e.g., badges, avatars) and real-world perks configured by instructors (e.g., extra time on an assignment, homework pass).
* The wallet tracks nugget balance and redemption history.
* Redemption is only possible if the student has sufficient nuggets.

### Acceptance Criteria

```gherkin
Given a student has earned nuggets in their wallet
When the student selects a reward item in the store
Then the nugget balance is reduced by the item's cost
And the student receives the reward (virtual item unlock or perk applied)

Given a student attempts to redeem an item without enough nuggets
When the student selects that item
Then the redemption is denied
And a message is shown indicating insufficient nuggets
```

**UML class diagram:** `experiments/project_14/class_diagram_114.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/redemption/Redemption.py` | `IfaceKind`, `ItemCost`, `NuggetBalance`, `RedemptionItem` |
| `src/domain/reward_item/RewardItem.py` | `IfaceKind`, `ItemCost`, `NuggetBalance`, `RedemptionItem` |
| `src/domain/reward_store/RewardStore.py` | `IfaceKind`, `ItemCost`, `NuggetBalance`, `RedemptionItem` |
| `src/repository/streak/streak_repository.py` | `IfaceKind` |
| `src/service/redemption/redemption_service.py` | `REQ_STU_01` |
| `src/service/reward_item/reward_item_service.py` | `REQ_STU_01` |
| `src/service/reward_store/reward_store_service.py` | `REQ_STU_01` |

---

### Task #115 — Cohort Leaderboard

**As a** student
**I need** a cohort leaderboard ranked by nuggets over a configurable window
**So that** I can track my progress and see how I compare with peers

### Details and Assumptions
* The leaderboard aggregates nuggets earned within a configurable time window (e.g., last 7 days, last 30 days).
* Students can opt out of appearing on the leaderboard.
* Instructors can disable the entire leaderboard for the cohort.

### Acceptance Criteria

```gherkin
Given the leaderboard is enabled by the instructor
And I have not opted out
When I view the cohort leaderboard
Then I see myself and other students ranked by total nuggets earned in the configured time window
```

**UML class diagram:** `experiments/project_14/class_diagram_115.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/domain/audit_event/AuditEvent.py` | `Permission`, `State` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission`, `State` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/domain/competency/Competency.py` | `Permission`, `Resource`, `State` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission`, `Resource`, `State` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Actor`, `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Actor`, `Permission` |
| `src/domain/question/Question.py` | `Permission`, `Resource`, `State` |
| `src/domain/redemption/Redemption.py` | `Actor`, `Interface`, `Resource` |
| `src/domain/reward_item/RewardItem.py` | `Actor`, `Interface`, `Resource` |
| `src/domain/reward_store/RewardStore.py` | `Actor`, `Interface`, `Resource` |
| `src/domain/student/Student.py` | `Student` |
| `src/domain/study_tip/StudyTip.py` | `Actor`, `Permission`, `Resource`, `State` |
| `src/repository/cohort_leaderboard/cohort_leaderboard_repository.py` | `Cohort_Settings_API`, `Leaderboard_Display`, `Student_Data_Store` |
| `src/repository/competency_breakdown/competency_breakdown_repository.py` | `Interface` |
| `src/repository/streak/streak_repository.py` | `Actor`, `Interface`, `Permission`, `Resource`, `State` |
| `src/repository/study_tip/study_tip_repository.py` | `Interface` |
| `src/service/attempt_review/attempt_review_service.py` | `Permission` |
| `src/service/cohort_leaderboard/cohort_leaderboard_service.py` | `REQ_COHORT_LEADERBOARD_01` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `Permission` |

---

### Task #116 — Past Attempt Review

**As a** student
**I need** to review past attempts with my answers, correct answers, nuggets per question, and competency trend charts
**So that** I can track my learning progress and identify areas needing improvement

### Details and Assumptions
* The feature displays a list of past attempts for the student.
* Each attempt includes per-question details: the student's answer, the correct answer, and an associated learning nugget.
* Competency trend charts show performance over time across different skills or topics.
* The review is accessible from the student's dashboard or a dedicated history page.

### Acceptance Criteria

```gherkin
Given I am a student with multiple completed attempts
When I navigate to the review section
Then I see a chronological list of my past attempts

Given I select a specific past attempt
When I view its details
Then I see for each question: my answer, the correct answer, and a learning nugget

Given I have sufficient attempt history
When I access the competency trend charts
Then I see graphical trends of my performance over time for each competency
```

**UML class diagram:** `experiments/project_14/class_diagram_116.puml`

**Files related to this task** (classes appear in UML diagram):

| File path | Matching classes |
|-----------|-----------------|
| `src/api/attempt_review/attempt_review_router.py` | `ReviewController` |
| `src/api/competency_trend_chart/competency_trend_chart_router.py` | `ReviewController` |
| `src/domain/attempt_review/AttemptReview.py` | `Attempt`, `ChartPoint` |
| `src/domain/audit_event/AuditEvent.py` | `Permission` |
| `src/domain/bonu_nugget_grant/BonuNuggetGrant.py` | `Permission` |
| `src/domain/cohort_leaderboard/CohortLeaderboard.py` | `Permission` |
| `src/domain/competency/Competency.py` | `Competency`, `Permission` |
| `src/domain/competency_breakdown/CompetencyBreakdown.py` | `Permission` |
| `src/domain/competency_trend_chart/CompetencyTrendChart.py` | `Attempt`, `ChartPoint` |
| `src/domain/exam_builder/ExamBuilder.py` | `Permission` |
| `src/domain/exam_session/ExamSession.py` | `Permission` |
| `src/domain/instructor/Instructor.py` | `Permission` |
| `src/domain/instructor_dashboard/InstructorDashboard.py` | `Permission` |
| `src/domain/question/Question.py` | `Permission`, `Question` |
| `src/domain/student/Student.py` | `Student` |
| `src/domain/study_tip/StudyTip.py` | `Permission` |
| `src/repository/attempt_review/attempt_review_repository.py` | `StudentDashboardUI`, `StudentDataAPI`, `StudentDataStore`, `TrendAPI` |
| `src/repository/competency_trend_chart/competency_trend_chart_repository.py` | `StudentDashboardUI`, `StudentDataAPI`, `StudentDataStore`, `TrendAPI` |
| `src/repository/streak/streak_repository.py` | `Permission` |
| `src/service/attempt_review/attempt_review_service.py` | `AccessControlService`, `DashboardData`, `PastAttemptData`, `Permission`, `ReviewService`, `Role`, `TrendData` |
| `src/service/competency_trend_chart/competency_trend_chart_service.py` | `AccessControlService`, `DashboardData`, `PastAttemptData`, `Permission`, `ReviewService`, `Role`, `TrendData` |

---
