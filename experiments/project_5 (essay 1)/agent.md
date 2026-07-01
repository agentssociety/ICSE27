# Project Agent Log

**Project ID:** 14
**Created:** 2026-06-29T15:01:58.729314
**Status:** Active

## Project Information

**Name:** Gamified Competency Assessment Platform
**Owner ID:** 1

**Description:**

5. Gamified Competency Assessment Platform

An educational platform where instructors design competency-based practice exams delivered to students in a gamified environment. Students earn nuggets by demonstrating mastery, while instructors gain rich analytics to evaluate individual and cohort competencies.

Core features:
- Let instructors register, log in, and manage a personal dashboard showing active exams, enrollment counts, and competency coverage
- Let instructors build exams with mixed question types (MCQ, drag-and-drop, code snippet) and tag - each question with one or more competencies
- Assign a difficulty tier (Beginner, Intermediate, Advanced) to each question that determines its nugget reward multiplier
- Let instructors schedule exams with an open date, a close date, and an optional per-attempt time limit enforced server-side
- Let instructors create cohorts, enroll students individually, and restrict each exam to one or more cohorts
- Show instructors a per-competency heatmap after each exam, highlighting competencies below a configurable mastery threshold in red
- Let instructors grant manual bonus nuggets to individual students with a written justification logged as an audit event
- Let students register and personalize a profile with an avatar, and display their nugget balance, earned badges, and competency radar chart
- Deliver exams to students one question at a time in a game-like interface with a live timer, progress bar, and animated nugget counter
- Build a streak system where consecutive correct answers apply a nugget multiplier (1.5×, 2×, 3×) that resets on any wrong answer
- Show students an instant competency breakdown after submission, flagging weak competencies with an study tip for each
- Maintain a nugget wallet per student redeemable in a reward store for virtual items or instructor-configured institutional perks
- Rank students on a cohort leaderboard by nuggets earned over a configurable window, with opt-out and instructor disable options
- Let students review every past attempt with their answers, correct answers, nuggets earned per question, and competency trend charts over time
- Enforce role-based access control across Admin, Instructor, and Student roles and write every sensitive action to an immutable audit log

## Project Configuration

| Key | Value |
|-----|-------|

## Artifacts Generated

> This section tracks all artifacts generated for this project

## Tasks

### Task #105
**Title:** Instructor Registration, Login, and Dashboard
**Summary:** [An instructor needs to register and log in to a personalized dashboard that displays active exams, enrollment counts, and competency coverage to manage courses and monitor student progress.]
**Created:** 2026-06-29T15:06:41.394968

---

### Task #106
**Title:** Exam Builder with Mixed Question Types
**Summary:** [An exam builder is needed that supports multiple choice, drag-and-drop, and code snippet questions, each tagged with competencies and a difficulty tier (Beginner, Intermediate, Advanced), plus a nugget reward multiplier to accurately test competencies and reward learning.]
**Created:** 2026-06-29T15:09:22.165726

---

### Task #107
**Title:** Exam Scheduling
**Summary:** [An instructor needs to schedule exams with open/close dates and an optional per-attempt time limit enforced server-side so that students can only access the exam within the specified time window and are limited to the allowed time per attempt.]
**Created:** 2026-06-29T15:12:51.927119

---

### Task #108
**Title:** Cohort Creation and Student Enrollment
**Summary:** Administrators can create cohorts, enroll individual students, and restrict exam access to specific cohorts for efficient group management and access control.
**Created:** 2026-06-29T15:13:57.726937

---

### Task #109
**Title:** Manual Bonus Nuggets Grant
**Summary:** [A teacher needs to manually grant bonus nuggets to students with a written justification, and the system logs each grant as an audit event for record-keeping.]
**Created:** 2026-06-29T15:15:01.009859

---

### Task #110
**Title:** Student Registration and Profile
**Summary:** [Student needs to register and have a personalized profile with avatar, nugget balance, badges, and competency radar chart to track progress and have a customized learning experience.]
**Created:** 2026-06-29T15:20:03.715874

---

### Task #111
**Title:** One-Question-at-a-Time Exam Delivery
**Summary:** [A student requires an exam system that displays one question per screen with a game-like interface, live timer, progress bar, and animated nugget counter to enhance engagement, track progress, and maintain motivation throughout the exam.]
**Created:** 2026-06-29T15:28:20.801871

---

### Task #112
**Title:** Streak System with Nugget Multiplier
**Summary:** [Implement a streak system where consecutive correct answers apply increasing nugget multipliers (1.5×, 2×, 3×), resetting to 1× on a wrong answer.]
**Created:** 2026-06-29T15:30:16.897306

---

### Task #113
**Title:** Instant Competency Breakdown
**Summary:** [The student requires an immediate competency breakdown after exam submission to identify weak areas and receive targeted study tips.]
**Created:** 2026-06-29T15:31:08.212729

---

### Task #114
**Title:** Student Nugget Wallet and Reward Store
**Summary:** [Students earn nuggets for achievements and can redeem them in a reward store for virtual items or instructor-configured perks, with the wallet tracking balance and ensuring sufficient nuggets for redemption.]
**Created:** 2026-06-29T15:33:29.305411

---

### Task #115
**Title:** Cohort Leaderboard
**Summary:** [A student needs a cohort leaderboard that ranks users by nuggets earned within a configurable time window, enabling progress tracking and peer comparison, with options to opt out or for instructors to disable it.]
**Created:** 2026-06-29T15:34:32.589886

---

### Task #116
**Title:** Past Attempt Review
**Summary:** [The student needs a feature to review past attempts with detailed per-question feedback and competency trend charts to track learning progress and identify areas for improvement.]
**Created:** 2026-06-29T15:38:40.603879

---

## Task Dependency Graph

**Updated:** 2026-06-29T16:11:00.910083
**Edge Direction:** Each key points to the tasks blocked by it.
**Method:** Dependencies are derived from shared domain/object models only.

### Dependency Analysis

Dependencies are inferred only from domain/object models.
Infrastructure, controllers, application services, APIs, UI, tests, and documentation are ignored.
The first task that introduces an object model owns it; later tasks can depend on that owner.

#### Task #105 - Instructor Registration, Login, and Dashboard
- Main object models: `Instructor`, `InstructorDashboard`
- Main object model aliases: `InstructorDashboard: Dashboard`
- Needed object models from other stories: `Exam`, `Enrollment`, `Competency`
- Needed object model aliases: `Competency: Skill`
- Needed tasks from other stories: `108`, `106`
- Direct dependencies kept in graph: `106`, `108`
- Needed object models without a matching owner: `Exam`
- Explanation: This task introduces Instructor and InstructorDashboard models. It needs Exam, Enrollment, and Competency models from other tasks to display active exams, enrollment counts, and competency coverage.

#### Task #106 - Exam Builder with Mixed Question Types
- Main object models: `ExamBuilder`, `Question`, `Competency`
- Main object model aliases: `Competency: Skill`
- Needed object models from other stories: None
- Needed tasks from other stories: None
- Direct dependencies kept in graph: None
- Explanation: This task owns ExamBuilder, Question, and Competency models. It does not need models from other tasks.

#### Task #107 - Exam Scheduling
- Main object models: `ExamSchedule`
- Main object model aliases: `ExamSchedule: Schedule, ExamScheduling`
- Needed object models from other stories: `Exam`, `Attempt`
- Needed tasks from other stories: None
- Direct dependencies kept in graph: None
- Needed object models without a matching owner: `Exam`, `Attempt`
- Explanation: This task introduces ExamSchedule. It needs Exam and Attempt models from other tasks to associate schedules with exams and track per-attempt time limits.

#### Task #108 - Cohort Creation and Student Enrollment
- Main object models: `Cohort`, `Enrollment`
- Main object model aliases: `Cohort: Group`, `Enrollment: StudentEnrollment`
- Needed object models from other stories: `Student`, `Exam`
- Needed tasks from other stories: `110`
- Direct dependencies kept in graph: `110`
- Needed object models without a matching owner: `Exam`
- Explanation: This task owns Cohort and Enrollment models. It needs Student and Exam models from other tasks to enroll students and restrict exams to cohorts.

#### Task #109 - Manual Bonus Nuggets Grant
- Main object models: `BonuNuggetGrant`, `AuditEvent`
- Main object model aliases: `BonuNuggetGrant: ManualBonuNugget, BonuGrant`, `AuditEvent: AuditLog, AuditEntry`
- Needed object models from other stories: `Teacher`, `Student`, `NuggetWallet`
- Needed object model aliases: `Teacher: Instructor`, `NuggetWallet: Wallet, NuggetBalance`
- Needed tasks from other stories: `105`, `110`
- Direct dependencies kept in graph: `105`
- Explanation: This task owns BonusNuggetGrant and AuditEvent models. It needs Teacher, Student, and NuggetWallet models from other tasks to record grants and update balances.

#### Task #110 - Student Registration and Profile
- Main object models: `Student`, `StudentProfile`, `NuggetWallet`, `Badge`, `CompetencyRadarChart`
- Main object model aliases: `StudentProfile: Profile, UserProfile`, `NuggetWallet: Wallet, NuggetBalance`, `CompetencyRadarChart: RadarChart, CompetencyChart`
- Needed object models from other stories: None
- Needed tasks from other stories: None
- Direct dependencies kept in graph: None
- Explanation: This task owns Student, StudentProfile, NuggetWallet, Badge, and CompetencyRadarChart models. It does not need models from other tasks.

#### Task #111 - One-Question-at-a-Time Exam Delivery
- Main object models: `ExamSession`
- Main object model aliases: `ExamSession: Session, ExamDelivery`
- Needed object models from other stories: `Exam`, `Question`, `Student`, `NuggetWallet`
- Needed object model aliases: `NuggetWallet: Wallet, NuggetBalance`
- Needed tasks from other stories: `106`, `110`
- Direct dependencies kept in graph: `106`, `110`
- Needed object models without a matching owner: `Exam`
- Explanation: This task owns ExamSession. It needs Exam, Question, Student, and NuggetWallet models from other tasks to deliver exams one question at a time and update nuggets.

#### Task #112 - Streak System with Nugget Multiplier
- Main object models: `Streak`
- Needed object models from other stories: `Student`, `NuggetWallet`
- Needed object model aliases: `NuggetWallet: Wallet, NuggetBalance`
- Needed tasks from other stories: `110`
- Direct dependencies kept in graph: `110`
- Explanation: This task owns Streak. It needs Student and NuggetWallet models from other tasks to track streaks and apply multipliers to nugget rewards.

#### Task #113 - Instant Competency Breakdown
- Main object models: `CompetencyBreakdown`, `StudyTip`
- Main object model aliases: `CompetencyBreakdown: Breakdown, CompetencyResult`, `StudyTip: Tip`
- Needed object models from other stories: `Exam`, `Attempt`, `Competency`
- Needed object model aliases: `Competency: Skill`
- Needed tasks from other stories: `106`
- Direct dependencies kept in graph: `106`
- Needed object models without a matching owner: `Exam`, `Attempt`
- Explanation: This task owns CompetencyBreakdown and StudyTip. It needs Exam, Attempt, and Competency models from other tasks to analyze results and generate study tips.

#### Task #114 - Student Nugget Wallet and Reward Store
- Main object models: `RewardStore`, `RewardItem`, `Redemption`
- Main object model aliases: `RewardStore: Store, RewardShop`, `RewardItem: Reward, Item, Perk`
- Needed object models from other stories: `Student`, `NuggetWallet`
- Needed object model aliases: `NuggetWallet: Wallet, NuggetBalance`
- Needed tasks from other stories: `110`
- Direct dependencies kept in graph: `110`
- Explanation: This task owns RewardStore, RewardItem, and Redemption models. It needs Student and NuggetWallet models from other tasks to manage purchases and deduct nuggets.

#### Task #115 - Cohort Leaderboard
- Main object models: `CohortLeaderboard`
- Main object model aliases: `CohortLeaderboard: Leaderboard, Ranking`
- Needed object models from other stories: `Cohort`, `Student`, `NuggetWallet`
- Needed object model aliases: `Cohort: Group`, `NuggetWallet: Wallet, NuggetBalance`
- Needed tasks from other stories: `108`, `110`
- Direct dependencies kept in graph: `108`
- Explanation: This task owns CohortLeaderboard. It needs Cohort, Student, and NuggetWallet models from other tasks to rank students by nuggets within a cohort.

#### Task #116 - Past Attempt Review
- Main object models: `AttemptReview`, `CompetencyTrendChart`
- Main object model aliases: `AttemptReview: Review, PastAttempt`, `CompetencyTrendChart: TrendChart, CompetencyTrend`
- Needed object models from other stories: `Attempt`, `Question`, `Competency`, `Student`
- Needed object model aliases: `Competency: Skill`
- Needed tasks from other stories: `106`, `110`
- Direct dependencies kept in graph: `106`, `110`
- Needed object models without a matching owner: `Attempt`
- Explanation: This task owns AttemptReview and CompetencyTrendChart. It needs Attempt, Question, Competency, and Student models from other tasks to display past attempts and competency trends.

### Graph

```json
{
  "105": [
    109
  ],
  "106": [
    105,
    111,
    113,
    116
  ],
  "107": [],
  "108": [
    105,
    115
  ],
  "109": [],
  "110": [
    108,
    111,
    112,
    114,
    116
  ],
  "111": [],
  "112": [],
  "113": [],
  "114": [],
  "115": [],
  "116": []
}
```

---

## Requirements

### Requirement #106
**Status:** Generated
**File:** experiments/project_14/requirement_106.json
**Generated:** 2026-06-29T16:14:39.867422
---

### Requirement #110
**Status:** Generated
**File:** experiments/project_14/requirement_110.json
**Generated:** 2026-06-29T16:16:15.224857
---

### Requirement #107
**Status:** Generated
**File:** experiments/project_14/requirement_107.json
**Generated:** 2026-06-29T16:18:33.254629
---

### Requirement #113
**Status:** Generated
**File:** experiments/project_14/requirement_113.json
**Generated:** 2026-06-29T16:20:11.252578
---

### Requirement #108
**Status:** Generated
**File:** experiments/project_14/requirement_108.json
**Generated:** 2026-06-29T16:22:21.104554
---

### Requirement #111
**Status:** Generated
**File:** experiments/project_14/requirement_111.json
**Generated:** 2026-06-29T16:24:23.877527
---

### Requirement #112
**Status:** Generated
**File:** experiments/project_14/requirement_112.json
**Generated:** 2026-06-29T16:28:01.883077
---

### Requirement #114
**Status:** Generated
**File:** experiments/project_14/requirement_114.json
**Generated:** 2026-06-29T16:29:49.899750
---

### Requirement #116
**Status:** Generated
**File:** experiments/project_14/requirement_116.json
**Generated:** 2026-06-29T16:31:58.137351
---

### Requirement #105
**Status:** Generated
**File:** experiments/project_14/requirement_105.json
**Generated:** 2026-06-29T16:34:13.021848
---

### Requirement #115
**Status:** Generated
**File:** experiments/project_14/requirement_115.json
**Generated:** 2026-06-29T16:36:47.694371
---

### Requirement #109
**Status:** Generated
**File:** experiments/project_14/requirement_109.json
**Generated:** 2026-06-29T16:38:52.852576
---

## Formal Specifications

### Formal Specification #110
**Status:** Generated
**File:** experiments/project_14/formal_spec_110.als
**Generated:** 2026-06-29T17:36:13.912805

---

### Formal Specification #113
**Status:** Generated
**File:** experiments/project_14/formal_spec_113.als
**Generated:** 2026-06-29T17:37:24.159439

---

### Formal Specification #106
**Status:** Generated
**File:** experiments/project_14/formal_spec_106.als
**Generated:** 2026-06-29T17:37:38.712018

---

### Formal Specification #108
**Status:** Generated
**File:** experiments/project_14/formal_spec_108.als
**Generated:** 2026-06-29T17:42:21.628924

---

### Formal Specification #107
**Status:** Generated
**File:** experiments/project_14/formal_spec_107.als
**Generated:** 2026-06-29T17:42:24.050270

---

### Formal Specification #111
**Status:** Generated
**File:** experiments/project_14/formal_spec_111.als
**Generated:** 2026-06-29T17:42:42.447604

---

### Formal Specification #112
**Status:** Generated
**File:** experiments/project_14/formal_spec_112.als
**Generated:** 2026-06-29T17:43:00.158147

---

### Formal Specification #105
**Status:** Generated
**File:** experiments/project_14/formal_spec_105.als
**Generated:** 2026-06-29T17:47:27.114705

---

### Formal Specification #116
**Status:** Generated
**File:** experiments/project_14/formal_spec_116.als
**Generated:** 2026-06-29T17:47:42.175284

---

### Formal Specification #115
**Status:** Generated
**File:** experiments/project_14/formal_spec_115.als
**Generated:** 2026-06-29T17:47:44.032882

---

### Formal Specification #114
**Status:** Generated
**File:** experiments/project_14/formal_spec_114.als
**Generated:** 2026-06-29T17:50:02.532674

---

### Formal Specification #109
**Status:** Generated
**File:** experiments/project_14/formal_spec_109.als
**Generated:** 2026-06-29T17:54:16.777343

---

## UML Diagrams

### UML Diagrams #106
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_106.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_106.puml`
**Generated:** 2026-06-29T17:57:16.664316
**Method injection:** 3 class(es) enriched — Competency (1 method(s)), DifficultyTag (1 method(s)), Question (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_106.puml`
- ✓ Sequence Diagram: `sequence_diagram_106.puml`

---

### UML Diagrams #110
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_110.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_110.puml`
**Generated:** 2026-06-29T17:58:49.837582
**Method injection:** 4 class(es) enriched — StudentAccount (2 method(s)), StudentProfile (2 method(s)), ProfileUI (1 method(s)), ValidationResult (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_110.puml`
- ✓ Sequence Diagram: `sequence_diagram_110.puml`

---

### UML Diagrams #107
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_107.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_107.puml`
**Generated:** 2026-06-29T18:00:33.880120
**Method injection:** 2 class(es) enriched — State (7 method(s)), Schedule (6 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_107.puml`
- ✓ Sequence Diagram: `sequence_diagram_107.puml`

---

### UML Diagrams #113
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_113.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_113.puml`
**Generated:** 2026-06-29T18:03:47.212013
**Method injection:** 2 class(es) enriched — REQ_EDU_01 (4 method(s)), State (4 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_113.puml`
- ✓ Sequence Diagram: `sequence_diagram_113.puml`

---

### UML Diagrams #108
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_108.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_108.puml`
**Generated:** 2026-06-29T18:04:59.921539
**Method injection:** 3 class(es) enriched — StudentCohortDatabase (4 method(s)), Cohort (1 method(s)), Exam (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_108.puml`
- ✓ Sequence Diagram: `sequence_diagram_108.puml`

---

### UML Diagrams #111
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_111.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_111.puml`
**Generated:** 2026-06-29T18:08:54.029602
**Method injection:** 8 class(es) enriched — Student (1 method(s)), Exam (1 method(s)), ExamSession (11 method(s)), Question (4 method(s)), ExamInterface (13 method(s)), NuggetWallet (1 method(s)), Instructor (1 method(s)), IT_Team (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_111.puml`
- ✓ Sequence Diagram: `sequence_diagram_111.puml`

---

### UML Diagrams #112
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_112.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_112.puml`
**Generated:** 2026-06-29T18:10:46.964292
**Method injection:** 7 class(es) enriched — GameInterface (1 method(s)), Operation (1 method(s)), Actor (1 method(s)), Resource (1 method(s)), Player (2 method(s)), Streak (2 method(s)), NuggetWallet (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_112.puml`
- ✓ Sequence Diagram: `sequence_diagram_112.puml`

---

### UML Diagrams #114
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_114.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_114.puml`
**Generated:** 2026-06-29T18:14:35.936890
**Method injection:** 4 class(es) enriched — REQ_STU_01 (5 method(s)), RedemptionItem (2 method(s)), NuggetBalance (2 method(s)), ItemCost (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_114.puml`
- ✓ Sequence Diagram: `sequence_diagram_114.puml`

---

### UML Diagrams #116
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_116.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_116.puml`
**Generated:** 2026-06-29T18:16:06.971855
**Method injection:** 7 class(es) enriched — Student (3 method(s)), DashboardData (2 method(s)), Attempt (2 method(s)), Question (3 method(s)), Competency (1 method(s)), ChartPoint (1 method(s)), PastAttemptData (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_116.puml`
- ✓ Sequence Diagram: `sequence_diagram_116.puml`

---

### UML Diagrams #105
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_105.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_105.puml`
**Generated:** 2026-06-29T18:17:08.207482
**Method injection:** 2 class(es) enriched — InstructorAccount (2 method(s)), DashboardContent (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_105.puml`
- ✓ Sequence Diagram: `sequence_diagram_105.puml`

---

### UML Diagrams #115
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_115.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_115.puml`
**Generated:** 2026-06-29T18:19:47.339078
**Method injection:** 5 class(es) enriched — REQ_COHORT_LEADERBOARD_01 (4 method(s)), Leaderboard_Display (8 method(s)), Actor (1 method(s)), Interface (1 method(s)), Resource (1 method(s))
**Artifacts:**
- ✓ Class Diagram: `class_diagram_115.puml`
- ✓ Sequence Diagram: `sequence_diagram_115.puml`

---

### UML Diagrams #109
**Status:** Generated
**Files:**
- Class Diagram: `experiments/project_14/class_diagram_109.puml`
- Sequence Diagram: `experiments/project_14/sequence_diagram_109.puml`
**Generated:** 2026-06-29T19:30:21.288892
**Method injection:** 0 class(es) enriched — 
**Artifacts:**
- ✓ Class Diagram: `class_diagram_109.puml`
- ✓ Sequence Diagram: `sequence_diagram_109.puml`

---

## Class Architecture

**Updated:** 2026-06-29T19:32:54.083763
**Total Domain Classes:** 25
**Implementation Order:** `ExamBuilder`, `Question`, `Competency`, `Schedule`, `Student`, `StudentProfile`, `NuggetWallet`, `Badge`, `RadarChart`, `CompetencyBreakdown`, `StudyTip`, `Cohort`, `Enrollment`, `AttemptReview`, `CompetencyTrendChart`, `ExamSession`, `Streak`, `RewardStore`, `RewardItem`, `Redemption`, `CohortLeaderboard`, `Instructor`, `InstructorDashboard`, `BonuNuggetGrant`, `AuditEvent`

### LLM Relationship Cardinality Corrections

- `Admin --|> Permission` → `Admin --|> Actor`: Admin is a type of Actor, not Permission. Inheritance from Actor is correct.
- `BonusNugget "0..1" ..> "1" AuditEvent` → `BonusNugget "1" --> "1" AuditEvent`: Each bonus nugget grant must be logged as an audit event, so a 1-to-1 directed association is more appropriate than a dependency with cardinalities.
- `Instructor ..> Dashboard_UI` → `Dashboard_UI ..> Instructor`: The UI depends on the Instructor model, not the other way around. Dependency direction should be from UI to domain class.
- `Instructor_Configuration_System --|> Interface` → `Instructor_Configuration_System ..> Interface`: The configuration system likely depends on an Interface, not inherits from it. Changing to dependency.
- `NuggetBalance "1" --> "1" Student` → `Student "1" --> "1" NuggetBalance`: A student owns a nugget balance; the association should originate from Student to NuggetBalance.
- `Resource *-- "1" Actor` → `Actor "1" --> "*" Resource`: An actor (e.g., Instructor) can own multiple resources; the composition was reversed. Changing to directed association with correct cardinality.
- `Schedule "1" -- "1" Date` → `Schedule "1" *-- "2" Date`: A schedule must have exactly two dates (open and close), so composition with multiplicity 2 is appropriate.
- `StudentProfile --> Badge` → `StudentProfile "1" --> "*" Badge`: A student profile can have multiple badges, so multiplicity should be many (0..* or *). Adding explicit multiplicity.

### Dependency Graph

```json
{
  "ExamBuilder": [],
  "Question": [
    "ExamSession",
    "AttemptReview",
    "CompetencyTrendChart"
  ],
  "Competency": [
    "CompetencyBreakdown",
    "StudyTip",
    "AttemptReview",
    "CompetencyTrendChart",
    "Instructor",
    "InstructorDashboard"
  ],
  "Schedule": [],
  "Student": [
    "Cohort",
    "Enrollment",
    "ExamSession",
    "Streak",
    "RewardStore",
    "RewardItem",
    "Redemption",
    "AttemptReview",
    "CompetencyTrendChart",
    "CohortLeaderboard",
    "BonuNuggetGrant",
    "AuditEvent"
  ],
  "StudentProfile": [],
  "NuggetWallet": [
    "ExamSession",
    "Streak",
    "RewardStore",
    "RewardItem",
    "Redemption",
    "CohortLeaderboard",
    "BonuNuggetGrant",
    "AuditEvent"
  ],
  "Badge": [],
  "RadarChart": [],
  "CompetencyBreakdown": [],
  "StudyTip": [],
  "Cohort": [
    "CohortLeaderboard"
  ],
  "Enrollment": [
    "Instructor",
    "InstructorDashboard"
  ],
  "ExamSession": [],
  "Streak": [],
  "RewardStore": [],
  "RewardItem": [],
  "Redemption": [],
  "AttemptReview": [],
  "CompetencyTrendChart": [],
  "Instructor": [
    "BonuNuggetGrant",
    "AuditEvent"
  ],
  "InstructorDashboard": [],
  "CohortLeaderboard": [],
  "BonuNuggetGrant": [],
  "AuditEvent": []
}
```

---

## Architecture Review

**Updated:** 2026-06-29T19:32:54.086682

### Architecture Corrections (auto-applied)

- **[missing_relationship]** Task #106 requires class ExamBuilder, but it is missing from the class list.
  - Fix: `add_relation` (affected_classes=['ExamBuilder'], new_relationship=ExamBuilder --|> (owns) Question, Competency)
- **[missing_relationship]** Task #113 requires classes CompetencyBreakdown and StudyTip, but they are missing.
  - Fix: `add_relation` (affected_classes=['CompetencyBreakdown', 'StudyTip'], new_relationship=CompetencyBreakdown --> StudyTip)
- **[missing_relationship]** Task #114 requires classes RewardStore, RewardItem, and Redemption, but they are missing.
  - Fix: `add_relation` (affected_classes=['RewardStore', 'RewardItem', 'Redemption'], new_relationship=RewardStore *-- RewardItem, Redemption --> RewardItem)
- **[missing_relationship]** Task #116 requires classes AttemptReview and CompetencyTrendChart, but they are missing.
  - Fix: `add_relation` (affected_classes=['AttemptReview', 'CompetencyTrendChart'], new_relationship=AttemptReview --> CompetencyTrendChart)
- **[missing_relationship]** Task #105 requires class InstructorDashboard, but it is missing.
  - Fix: `add_relation` (affected_classes=['InstructorDashboard'], new_relationship=Instructor -- InstructorDashboard)
- **[duplicate_concept]** Player and Student represent the same concept; Player should be merged into Student or removed.
  - Fix: `merge_classes` (keep=Student, remove=Player, transfer_relationships=['Player to NuggetWallet composition', 'Player to Streak composition', 'Player to Question association'])
- **[duplicate_concept]** Teacher and Instructor represent the same role; Teacher should be merged into Instructor.
  - Fix: `merge_classes` (keep=Instructor, remove=Teacher, transfer_relationships=['Teacher to BonusNugget association'])
- **[duplicate_concept]** BonusNugget and BonusNuggetGrant (from Task #109) are the same; rename BonusNugget to BonusNuggetGrant or merge.
  - Fix: `merge_classes` (keep=BonusNuggetGrant, remove=BonusNugget, transfer_relationships=['BonusNugget to AuditEvent', 'BonusNugget to Justification', 'Student to BonusNugget', 'Teacher to BonusNugget'])
- **[other_correction]** Student has both a composition relationship and a directed association to NuggetWallet; this is redundant and should be unified.
  - Fix: `remove_relation` (affected_classes=['Student', 'NuggetWallet'], remove_arrow=Student --> NuggetWallet (directed association) or keep one)

### Architecture Suggestions (human review)

1. **[rename_for_clarity]** Rename Player to Student to align with ubiquitous language from tasks.
   - Affects: `Player`
2. **[rename_for_clarity]** Rename Teacher to Instructor to match task descriptions.
   - Affects: `Teacher`
3. **[rename_for_clarity]** Rename BonusNugget to BonusNuggetGrant to match Task #109.
   - Affects: `BonusNugget`
4. **[introduce_value_object]** Introduce a value object DifficultyTier (enum: Beginner, Intermediate, Advanced) to replace the primitive attribute on Question.
   - Affects: `Question`
5. **[introduce_value_object]** Introduce a value object NuggetMultiplier to encapsulate the multiplier logic (1x, 1.5x, 2x, 3x).
   - Affects: `Streak`
6. **[general]** Consider removing generic or infrastructural classes (State, Permission, Resource, Actor, Interface, User_Database, REQ_*) from the domain model if they are not core to the business logic, to keep the model focused.
   - Affects: `State`, `Permission`, `Resource`, `Actor`, `Interface`, `User_Database`, `REQ_*`

---

## Package Design

### Package: `domain.exam_builder`
**Layer:** domain
**Path:** `src/domain/exam_builder`
**Description:** Domain layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** None
**Files:**
  - `ExamBuilder.py` — `ExamBuilder`, `ExamBuilderId`, `ExamBuilderCreatedEvent`, `ExamBuilderUpdatedEvent`

---

### Package: `dto.exam_builder`
**Layer:** dto
**Path:** `src/dto/exam_builder`
**Description:** Dto layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`
**Files:**
  - `exam_builder_dto.py` — `ExamBuilderCreateRequest`, `ExamBuilderUpdateRequest`, `ExamBuilderResponse`

---

### Package: `repository.exam_builder`
**Layer:** repository
**Path:** `src/repository/exam_builder`
**Description:** Repository layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`
**Files:**
  - `exam_builder_repository.py` — `ExamBuilderRepository`

---

### Package: `orm.exam_builder`
**Layer:** orm
**Path:** `src/orm/exam_builder`
**Description:** Orm layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`
**Files:**
  - `exam_builder_orm.py` — `ExamBuilderORM`

---

### Package: `infra.exam_builder`
**Layer:** infra
**Path:** `src/infra/exam_builder`
**Description:** Infra layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `repository.exam_builder`, `orm.exam_builder`
**Files:**
  - `exam_builder_repo_impl.py` — `SQLAlchemyExamBuilderRepository`

---

### Package: `service.exam_builder`
**Layer:** service
**Path:** `src/service/exam_builder`
**Description:** Service layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `repository.exam_builder`, `dto.exam_builder`
**Files:**
  - `exam_builder_service.py` — `ExamBuilderService`, `ExamBuilderServiceImpl`

---

### Package: `api.exam_builder`
**Layer:** api
**Path:** `src/api/exam_builder`
**Description:** Api layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `service.exam_builder`, `dto.exam_builder`
**Files:**
  - `exam_builder_router.py` — `ExamBuilderRouter`

---

### Package: `domain.question`
**Layer:** domain
**Path:** `src/domain/question`
**Description:** Domain layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** None
**Files:**
  - `Question.py` — `Question`, `QuestionId`, `QuestionCreatedEvent`, `QuestionUpdatedEvent`

---

### Package: `dto.question`
**Layer:** dto
**Path:** `src/dto/question`
**Description:** Dto layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_dto.py` — `QuestionCreateRequest`, `QuestionUpdateRequest`, `QuestionResponse`

---

### Package: `repository.question`
**Layer:** repository
**Path:** `src/repository/question`
**Description:** Repository layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_repository.py` — `QuestionRepository`

---

### Package: `orm.question`
**Layer:** orm
**Path:** `src/orm/question`
**Description:** Orm layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_orm.py` — `QuestionORM`

---

### Package: `infra.question`
**Layer:** infra
**Path:** `src/infra/question`
**Description:** Infra layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `repository.question`, `orm.question`
**Files:**
  - `question_repo_impl.py` — `SQLAlchemyQuestionRepository`

---

### Package: `service.question`
**Layer:** service
**Path:** `src/service/question`
**Description:** Service layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `repository.question`, `dto.question`
**Files:**
  - `question_service.py` — `QuestionService`, `QuestionServiceImpl`

---

### Package: `api.question`
**Layer:** api
**Path:** `src/api/question`
**Description:** Api layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `service.question`, `dto.question`
**Files:**
  - `question_router.py` — `QuestionRouter`

---

### Package: `domain.competency`
**Layer:** domain
**Path:** `src/domain/competency`
**Description:** Domain layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** None
**Files:**
  - `Competency.py` — `Competency`, `CompetencyId`, `CompetencyCreatedEvent`, `CompetencyUpdatedEvent`

---

### Package: `dto.competency`
**Layer:** dto
**Path:** `src/dto/competency`
**Description:** Dto layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`
**Files:**
  - `competency_dto.py` — `CompetencyCreateRequest`, `CompetencyUpdateRequest`, `CompetencyResponse`

---

### Package: `repository.competency`
**Layer:** repository
**Path:** `src/repository/competency`
**Description:** Repository layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`
**Files:**
  - `competency_repository.py` — `CompetencyRepository`

---

### Package: `orm.competency`
**Layer:** orm
**Path:** `src/orm/competency`
**Description:** Orm layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`
**Files:**
  - `competency_orm.py` — `CompetencyORM`

---

### Package: `infra.competency`
**Layer:** infra
**Path:** `src/infra/competency`
**Description:** Infra layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `repository.competency`, `orm.competency`
**Files:**
  - `competency_repo_impl.py` — `SQLAlchemyCompetencyRepository`

---

### Package: `service.competency`
**Layer:** service
**Path:** `src/service/competency`
**Description:** Service layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `repository.competency`, `dto.competency`
**Files:**
  - `competency_service.py` — `CompetencyService`, `CompetencyServiceImpl`

---

### Package: `api.competency`
**Layer:** api
**Path:** `src/api/competency`
**Description:** Api layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `service.competency`, `dto.competency`
**Files:**
  - `competency_router.py` — `CompetencyRouter`

---

### Package: `domain.schedule`
**Layer:** domain
**Path:** `src/domain/schedule`
**Description:** Domain layer for the Schedule domain class
**Tasks:** None
**Depends on:** None
**Files:**
  - `Schedule.py` — `Schedule`, `ScheduleId`, `ScheduleCreatedEvent`, `ScheduleUpdatedEvent`

---

### Package: `dto.schedule`
**Layer:** dto
**Path:** `src/dto/schedule`
**Description:** Dto layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_dto.py` — `ScheduleCreateRequest`, `ScheduleUpdateRequest`, `ScheduleResponse`

---

### Package: `repository.schedule`
**Layer:** repository
**Path:** `src/repository/schedule`
**Description:** Repository layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_repository.py` — `ScheduleRepository`

---

### Package: `orm.schedule`
**Layer:** orm
**Path:** `src/orm/schedule`
**Description:** Orm layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_orm.py` — `ScheduleORM`

---

### Package: `infra.schedule`
**Layer:** infra
**Path:** `src/infra/schedule`
**Description:** Infra layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`, `repository.schedule`, `orm.schedule`
**Files:**
  - `schedule_repo_impl.py` — `SQLAlchemyScheduleRepository`

---

### Package: `service.schedule`
**Layer:** service
**Path:** `src/service/schedule`
**Description:** Service layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`, `repository.schedule`, `dto.schedule`
**Files:**
  - `schedule_service.py` — `ScheduleService`, `ScheduleServiceImpl`

---

### Package: `api.schedule`
**Layer:** api
**Path:** `src/api/schedule`
**Description:** Api layer for the Schedule domain class
**Tasks:** None
**Depends on:** `service.schedule`, `dto.schedule`
**Files:**
  - `schedule_router.py` — `ScheduleRouter`

---

### Package: `domain.student`
**Layer:** domain
**Path:** `src/domain/student`
**Description:** Domain layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** None
**Files:**
  - `Student.py` — `Student`, `StudentId`, `StudentCreatedEvent`, `StudentUpdatedEvent`

---

### Package: `dto.student`
**Layer:** dto
**Path:** `src/dto/student`
**Description:** Dto layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_dto.py` — `StudentCreateRequest`, `StudentUpdateRequest`, `StudentResponse`

---

### Package: `repository.student`
**Layer:** repository
**Path:** `src/repository/student`
**Description:** Repository layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_repository.py` — `StudentRepository`

---

### Package: `orm.student`
**Layer:** orm
**Path:** `src/orm/student`
**Description:** Orm layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_orm.py` — `StudentORM`

---

### Package: `infra.student`
**Layer:** infra
**Path:** `src/infra/student`
**Description:** Infra layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `repository.student`, `orm.student`
**Files:**
  - `student_repo_impl.py` — `SQLAlchemyStudentRepository`

---

### Package: `service.student`
**Layer:** service
**Path:** `src/service/student`
**Description:** Service layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `repository.student`, `dto.student`
**Files:**
  - `student_service.py` — `StudentService`, `StudentServiceImpl`

---

### Package: `api.student`
**Layer:** api
**Path:** `src/api/student`
**Description:** Api layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `service.student`, `dto.student`
**Files:**
  - `student_router.py` — `StudentRouter`

---

### Package: `domain.student_profile`
**Layer:** domain
**Path:** `src/domain/student_profile`
**Description:** Domain layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** None
**Files:**
  - `StudentProfile.py` — `StudentProfile`, `StudentProfileId`, `StudentProfileCreatedEvent`, `StudentProfileUpdatedEvent`

---

### Package: `dto.student_profile`
**Layer:** dto
**Path:** `src/dto/student_profile`
**Description:** Dto layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_dto.py` — `StudentProfileCreateRequest`, `StudentProfileUpdateRequest`, `StudentProfileResponse`

---

### Package: `repository.student_profile`
**Layer:** repository
**Path:** `src/repository/student_profile`
**Description:** Repository layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_repository.py` — `StudentProfileRepository`

---

### Package: `orm.student_profile`
**Layer:** orm
**Path:** `src/orm/student_profile`
**Description:** Orm layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_orm.py` — `StudentProfileORM`

---

### Package: `infra.student_profile`
**Layer:** infra
**Path:** `src/infra/student_profile`
**Description:** Infra layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`, `repository.student_profile`, `orm.student_profile`
**Files:**
  - `student_profile_repo_impl.py` — `SQLAlchemyStudentProfileRepository`

---

### Package: `service.student_profile`
**Layer:** service
**Path:** `src/service/student_profile`
**Description:** Service layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`, `repository.student_profile`, `dto.student_profile`
**Files:**
  - `student_profile_service.py` — `StudentProfileService`, `StudentProfileServiceImpl`

---

### Package: `api.student_profile`
**Layer:** api
**Path:** `src/api/student_profile`
**Description:** Api layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `service.student_profile`, `dto.student_profile`
**Files:**
  - `student_profile_router.py` — `StudentProfileRouter`

---

### Package: `domain.nugget_wallet`
**Layer:** domain
**Path:** `src/domain/nugget_wallet`
**Description:** Domain layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** None
**Files:**
  - `NuggetWallet.py` — `NuggetWallet`, `NuggetWalletId`, `NuggetWalletCreatedEvent`, `NuggetWalletUpdatedEvent`

---

### Package: `dto.nugget_wallet`
**Layer:** dto
**Path:** `src/dto/nugget_wallet`
**Description:** Dto layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_dto.py` — `NuggetWalletCreateRequest`, `NuggetWalletUpdateRequest`, `NuggetWalletResponse`

---

### Package: `repository.nugget_wallet`
**Layer:** repository
**Path:** `src/repository/nugget_wallet`
**Description:** Repository layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_repository.py` — `NuggetWalletRepository`

---

### Package: `orm.nugget_wallet`
**Layer:** orm
**Path:** `src/orm/nugget_wallet`
**Description:** Orm layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_orm.py` — `NuggetWalletORM`

---

### Package: `infra.nugget_wallet`
**Layer:** infra
**Path:** `src/infra/nugget_wallet`
**Description:** Infra layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `repository.nugget_wallet`, `orm.nugget_wallet`
**Files:**
  - `nugget_wallet_repo_impl.py` — `SQLAlchemyNuggetWalletRepository`

---

### Package: `service.nugget_wallet`
**Layer:** service
**Path:** `src/service/nugget_wallet`
**Description:** Service layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `repository.nugget_wallet`, `dto.nugget_wallet`
**Files:**
  - `nugget_wallet_service.py` — `NuggetWalletService`, `NuggetWalletServiceImpl`

---

### Package: `api.nugget_wallet`
**Layer:** api
**Path:** `src/api/nugget_wallet`
**Description:** Api layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `service.nugget_wallet`, `dto.nugget_wallet`
**Files:**
  - `nugget_wallet_router.py` — `NuggetWalletRouter`

---

### Package: `domain.badge`
**Layer:** domain
**Path:** `src/domain/badge`
**Description:** Domain layer for the Badge domain class
**Tasks:** #110
**Depends on:** None
**Files:**
  - `Badge.py` — `Badge`, `BadgeId`, `BadgeCreatedEvent`, `BadgeUpdatedEvent`

---

### Package: `dto.badge`
**Layer:** dto
**Path:** `src/dto/badge`
**Description:** Dto layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_dto.py` — `BadgeCreateRequest`, `BadgeUpdateRequest`, `BadgeResponse`

---

### Package: `repository.badge`
**Layer:** repository
**Path:** `src/repository/badge`
**Description:** Repository layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_repository.py` — `BadgeRepository`

---

### Package: `orm.badge`
**Layer:** orm
**Path:** `src/orm/badge`
**Description:** Orm layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_orm.py` — `BadgeORM`

---

### Package: `infra.badge`
**Layer:** infra
**Path:** `src/infra/badge`
**Description:** Infra layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`, `repository.badge`, `orm.badge`
**Files:**
  - `badge_repo_impl.py` — `SQLAlchemyBadgeRepository`

---

### Package: `service.badge`
**Layer:** service
**Path:** `src/service/badge`
**Description:** Service layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`, `repository.badge`, `dto.badge`
**Files:**
  - `badge_service.py` — `BadgeService`, `BadgeServiceImpl`

---

### Package: `api.badge`
**Layer:** api
**Path:** `src/api/badge`
**Description:** Api layer for the Badge domain class
**Tasks:** #110
**Depends on:** `service.badge`, `dto.badge`
**Files:**
  - `badge_router.py` — `BadgeRouter`

---

### Package: `domain.radar_chart`
**Layer:** domain
**Path:** `src/domain/radar_chart`
**Description:** Domain layer for the RadarChart domain class
**Tasks:** None
**Depends on:** None
**Files:**
  - `RadarChart.py` — `RadarChart`, `RadarChartId`, `RadarChartCreatedEvent`, `RadarChartUpdatedEvent`

---

### Package: `dto.radar_chart`
**Layer:** dto
**Path:** `src/dto/radar_chart`
**Description:** Dto layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_dto.py` — `RadarChartCreateRequest`, `RadarChartUpdateRequest`, `RadarChartResponse`

---

### Package: `repository.radar_chart`
**Layer:** repository
**Path:** `src/repository/radar_chart`
**Description:** Repository layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_repository.py` — `RadarChartRepository`

---

### Package: `orm.radar_chart`
**Layer:** orm
**Path:** `src/orm/radar_chart`
**Description:** Orm layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_orm.py` — `RadarChartORM`

---

### Package: `infra.radar_chart`
**Layer:** infra
**Path:** `src/infra/radar_chart`
**Description:** Infra layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`, `repository.radar_chart`, `orm.radar_chart`
**Files:**
  - `radar_chart_repo_impl.py` — `SQLAlchemyRadarChartRepository`

---

### Package: `service.radar_chart`
**Layer:** service
**Path:** `src/service/radar_chart`
**Description:** Service layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`, `repository.radar_chart`, `dto.radar_chart`
**Files:**
  - `radar_chart_service.py` — `RadarChartService`, `RadarChartServiceImpl`

---

### Package: `api.radar_chart`
**Layer:** api
**Path:** `src/api/radar_chart`
**Description:** Api layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `service.radar_chart`, `dto.radar_chart`
**Files:**
  - `radar_chart_router.py` — `RadarChartRouter`

---

### Package: `domain.competency_breakdown`
**Layer:** domain
**Path:** `src/domain/competency_breakdown`
**Description:** Domain layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** None
**Files:**
  - `CompetencyBreakdown.py` — `CompetencyBreakdown`, `CompetencyBreakdownId`, `CompetencyBreakdownCreatedEvent`, `CompetencyBreakdownUpdatedEvent`

---

### Package: `dto.competency_breakdown`
**Layer:** dto
**Path:** `src/dto/competency_breakdown`
**Description:** Dto layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`
**Files:**
  - `competency_breakdown_dto.py` — `CompetencyBreakdownCreateRequest`, `CompetencyBreakdownUpdateRequest`, `CompetencyBreakdownResponse`

---

### Package: `repository.competency_breakdown`
**Layer:** repository
**Path:** `src/repository/competency_breakdown`
**Description:** Repository layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`
**Files:**
  - `competency_breakdown_repository.py` — `CompetencyBreakdownRepository`

---

### Package: `orm.competency_breakdown`
**Layer:** orm
**Path:** `src/orm/competency_breakdown`
**Description:** Orm layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`
**Files:**
  - `competency_breakdown_orm.py` — `CompetencyBreakdownORM`

---

### Package: `infra.competency_breakdown`
**Layer:** infra
**Path:** `src/infra/competency_breakdown`
**Description:** Infra layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `repository.competency_breakdown`, `orm.competency_breakdown`
**Files:**
  - `competency_breakdown_repo_impl.py` — `SQLAlchemyCompetencyBreakdownRepository`

---

### Package: `service.competency_breakdown`
**Layer:** service
**Path:** `src/service/competency_breakdown`
**Description:** Service layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `repository.competency_breakdown`, `dto.competency_breakdown`, `service.competency`
**Files:**
  - `competency_breakdown_service.py` — `CompetencyBreakdownService`, `CompetencyBreakdownServiceImpl`

---

### Package: `api.competency_breakdown`
**Layer:** api
**Path:** `src/api/competency_breakdown`
**Description:** Api layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `service.competency_breakdown`, `dto.competency_breakdown`
**Files:**
  - `competency_breakdown_router.py` — `CompetencyBreakdownRouter`

---

### Package: `domain.study_tip`
**Layer:** domain
**Path:** `src/domain/study_tip`
**Description:** Domain layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** None
**Files:**
  - `StudyTip.py` — `StudyTip`, `StudyTipId`, `StudyTipCreatedEvent`, `StudyTipUpdatedEvent`

---

### Package: `dto.study_tip`
**Layer:** dto
**Path:** `src/dto/study_tip`
**Description:** Dto layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`
**Files:**
  - `study_tip_dto.py` — `StudyTipCreateRequest`, `StudyTipUpdateRequest`, `StudyTipResponse`

---

### Package: `repository.study_tip`
**Layer:** repository
**Path:** `src/repository/study_tip`
**Description:** Repository layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`
**Files:**
  - `study_tip_repository.py` — `StudyTipRepository`

---

### Package: `orm.study_tip`
**Layer:** orm
**Path:** `src/orm/study_tip`
**Description:** Orm layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`
**Files:**
  - `study_tip_orm.py` — `StudyTipORM`

---

### Package: `infra.study_tip`
**Layer:** infra
**Path:** `src/infra/study_tip`
**Description:** Infra layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`, `repository.study_tip`, `orm.study_tip`
**Files:**
  - `study_tip_repo_impl.py` — `SQLAlchemyStudyTipRepository`

---

### Package: `service.study_tip`
**Layer:** service
**Path:** `src/service/study_tip`
**Description:** Service layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`, `repository.study_tip`, `dto.study_tip`, `service.competency`
**Files:**
  - `study_tip_service.py` — `StudyTipService`, `StudyTipServiceImpl`

---

### Package: `api.study_tip`
**Layer:** api
**Path:** `src/api/study_tip`
**Description:** Api layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `service.study_tip`, `dto.study_tip`
**Files:**
  - `study_tip_router.py` — `StudyTipRouter`

---

### Package: `domain.cohort`
**Layer:** domain
**Path:** `src/domain/cohort`
**Description:** Domain layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** None
**Files:**
  - `Cohort.py` — `Cohort`, `CohortId`, `CohortCreatedEvent`, `CohortUpdatedEvent`

---

### Package: `dto.cohort`
**Layer:** dto
**Path:** `src/dto/cohort`
**Description:** Dto layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_dto.py` — `CohortCreateRequest`, `CohortUpdateRequest`, `CohortResponse`

---

### Package: `repository.cohort`
**Layer:** repository
**Path:** `src/repository/cohort`
**Description:** Repository layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_repository.py` — `CohortRepository`

---

### Package: `orm.cohort`
**Layer:** orm
**Path:** `src/orm/cohort`
**Description:** Orm layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_orm.py` — `CohortORM`

---

### Package: `infra.cohort`
**Layer:** infra
**Path:** `src/infra/cohort`
**Description:** Infra layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `repository.cohort`, `orm.cohort`
**Files:**
  - `cohort_repo_impl.py` — `SQLAlchemyCohortRepository`

---

### Package: `service.cohort`
**Layer:** service
**Path:** `src/service/cohort`
**Description:** Service layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `repository.cohort`, `dto.cohort`, `service.student`
**Files:**
  - `cohort_service.py` — `CohortService`, `CohortServiceImpl`

---

### Package: `api.cohort`
**Layer:** api
**Path:** `src/api/cohort`
**Description:** Api layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `service.cohort`, `dto.cohort`
**Files:**
  - `cohort_router.py` — `CohortRouter`

---

### Package: `domain.enrollment`
**Layer:** domain
**Path:** `src/domain/enrollment`
**Description:** Domain layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** None
**Files:**
  - `Enrollment.py` — `Enrollment`, `EnrollmentId`, `EnrollmentCreatedEvent`, `EnrollmentUpdatedEvent`

---

### Package: `dto.enrollment`
**Layer:** dto
**Path:** `src/dto/enrollment`
**Description:** Dto layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_dto.py` — `EnrollmentCreateRequest`, `EnrollmentUpdateRequest`, `EnrollmentResponse`

---

### Package: `repository.enrollment`
**Layer:** repository
**Path:** `src/repository/enrollment`
**Description:** Repository layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_repository.py` — `EnrollmentRepository`

---

### Package: `orm.enrollment`
**Layer:** orm
**Path:** `src/orm/enrollment`
**Description:** Orm layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_orm.py` — `EnrollmentORM`

---

### Package: `infra.enrollment`
**Layer:** infra
**Path:** `src/infra/enrollment`
**Description:** Infra layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `repository.enrollment`, `orm.enrollment`
**Files:**
  - `enrollment_repo_impl.py` — `SQLAlchemyEnrollmentRepository`

---

### Package: `service.enrollment`
**Layer:** service
**Path:** `src/service/enrollment`
**Description:** Service layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `repository.enrollment`, `dto.enrollment`, `service.student`
**Files:**
  - `enrollment_service.py` — `EnrollmentService`, `EnrollmentServiceImpl`

---

### Package: `api.enrollment`
**Layer:** api
**Path:** `src/api/enrollment`
**Description:** Api layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `service.enrollment`, `dto.enrollment`
**Files:**
  - `enrollment_router.py` — `EnrollmentRouter`

---

### Package: `domain.attempt_review`
**Layer:** domain
**Path:** `src/domain/attempt_review`
**Description:** Domain layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** None
**Files:**
  - `AttemptReview.py` — `AttemptReview`, `AttemptReviewId`, `AttemptReviewCreatedEvent`, `AttemptReviewUpdatedEvent`

---

### Package: `dto.attempt_review`
**Layer:** dto
**Path:** `src/dto/attempt_review`
**Description:** Dto layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`
**Files:**
  - `attempt_review_dto.py` — `AttemptReviewCreateRequest`, `AttemptReviewUpdateRequest`, `AttemptReviewResponse`

---

### Package: `repository.attempt_review`
**Layer:** repository
**Path:** `src/repository/attempt_review`
**Description:** Repository layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`
**Files:**
  - `attempt_review_repository.py` — `AttemptReviewRepository`

---

### Package: `orm.attempt_review`
**Layer:** orm
**Path:** `src/orm/attempt_review`
**Description:** Orm layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`
**Files:**
  - `attempt_review_orm.py` — `AttemptReviewORM`

---

### Package: `infra.attempt_review`
**Layer:** infra
**Path:** `src/infra/attempt_review`
**Description:** Infra layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `repository.attempt_review`, `orm.attempt_review`
**Files:**
  - `attempt_review_repo_impl.py` — `SQLAlchemyAttemptReviewRepository`

---

### Package: `service.attempt_review`
**Layer:** service
**Path:** `src/service/attempt_review`
**Description:** Service layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `repository.attempt_review`, `dto.attempt_review`, `service.question`, `service.competency`, `service.student`
**Files:**
  - `attempt_review_service.py` — `AttemptReviewService`, `AttemptReviewServiceImpl`

---

### Package: `api.attempt_review`
**Layer:** api
**Path:** `src/api/attempt_review`
**Description:** Api layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `service.attempt_review`, `dto.attempt_review`
**Files:**
  - `attempt_review_router.py` — `AttemptReviewRouter`

---

### Package: `domain.competency_trend_chart`
**Layer:** domain
**Path:** `src/domain/competency_trend_chart`
**Description:** Domain layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** None
**Files:**
  - `CompetencyTrendChart.py` — `CompetencyTrendChart`, `CompetencyTrendChartId`, `CompetencyTrendChartCreatedEvent`, `CompetencyTrendChartUpdatedEvent`

---

### Package: `dto.competency_trend_chart`
**Layer:** dto
**Path:** `src/dto/competency_trend_chart`
**Description:** Dto layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`
**Files:**
  - `competency_trend_chart_dto.py` — `CompetencyTrendChartCreateRequest`, `CompetencyTrendChartUpdateRequest`, `CompetencyTrendChartResponse`

---

### Package: `repository.competency_trend_chart`
**Layer:** repository
**Path:** `src/repository/competency_trend_chart`
**Description:** Repository layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`
**Files:**
  - `competency_trend_chart_repository.py` — `CompetencyTrendChartRepository`

---

### Package: `orm.competency_trend_chart`
**Layer:** orm
**Path:** `src/orm/competency_trend_chart`
**Description:** Orm layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`
**Files:**
  - `competency_trend_chart_orm.py` — `CompetencyTrendChartORM`

---

### Package: `infra.competency_trend_chart`
**Layer:** infra
**Path:** `src/infra/competency_trend_chart`
**Description:** Infra layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`, `repository.competency_trend_chart`, `orm.competency_trend_chart`
**Files:**
  - `competency_trend_chart_repo_impl.py` — `SQLAlchemyCompetencyTrendChartRepository`

---

### Package: `service.competency_trend_chart`
**Layer:** service
**Path:** `src/service/competency_trend_chart`
**Description:** Service layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`, `repository.competency_trend_chart`, `dto.competency_trend_chart`, `service.question`, `service.competency`, `service.student`
**Files:**
  - `competency_trend_chart_service.py` — `CompetencyTrendChartService`, `CompetencyTrendChartServiceImpl`

---

### Package: `api.competency_trend_chart`
**Layer:** api
**Path:** `src/api/competency_trend_chart`
**Description:** Api layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `service.competency_trend_chart`, `dto.competency_trend_chart`
**Files:**
  - `competency_trend_chart_router.py` — `CompetencyTrendChartRouter`

---

### Package: `domain.exam_session`
**Layer:** domain
**Path:** `src/domain/exam_session`
**Description:** Domain layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** None
**Files:**
  - `ExamSession.py` — `ExamSession`, `ExamSessionId`, `ExamSessionCreatedEvent`, `ExamSessionUpdatedEvent`

---

### Package: `dto.exam_session`
**Layer:** dto
**Path:** `src/dto/exam_session`
**Description:** Dto layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_dto.py` — `ExamSessionCreateRequest`, `ExamSessionUpdateRequest`, `ExamSessionResponse`

---

### Package: `repository.exam_session`
**Layer:** repository
**Path:** `src/repository/exam_session`
**Description:** Repository layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_repository.py` — `ExamSessionRepository`

---

### Package: `orm.exam_session`
**Layer:** orm
**Path:** `src/orm/exam_session`
**Description:** Orm layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_orm.py` — `ExamSessionORM`

---

### Package: `infra.exam_session`
**Layer:** infra
**Path:** `src/infra/exam_session`
**Description:** Infra layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`, `repository.exam_session`, `orm.exam_session`
**Files:**
  - `exam_session_repo_impl.py` — `SQLAlchemyExamSessionRepository`

---

### Package: `service.exam_session`
**Layer:** service
**Path:** `src/service/exam_session`
**Description:** Service layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`, `repository.exam_session`, `dto.exam_session`, `service.question`, `service.student`, `service.nugget_wallet`
**Files:**
  - `exam_session_service.py` — `ExamSessionService`, `ExamSessionServiceImpl`

---

### Package: `api.exam_session`
**Layer:** api
**Path:** `src/api/exam_session`
**Description:** Api layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `service.exam_session`, `dto.exam_session`
**Files:**
  - `exam_session_router.py` — `ExamSessionRouter`

---

### Package: `domain.streak`
**Layer:** domain
**Path:** `src/domain/streak`
**Description:** Domain layer for the Streak domain class
**Tasks:** #112
**Depends on:** None
**Files:**
  - `Streak.py` — `Streak`, `StreakId`, `StreakCreatedEvent`, `StreakUpdatedEvent`

---

### Package: `dto.streak`
**Layer:** dto
**Path:** `src/dto/streak`
**Description:** Dto layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_dto.py` — `StreakCreateRequest`, `StreakUpdateRequest`, `StreakResponse`

---

### Package: `repository.streak`
**Layer:** repository
**Path:** `src/repository/streak`
**Description:** Repository layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_repository.py` — `StreakRepository`

---

### Package: `orm.streak`
**Layer:** orm
**Path:** `src/orm/streak`
**Description:** Orm layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_orm.py` — `StreakORM`

---

### Package: `infra.streak`
**Layer:** infra
**Path:** `src/infra/streak`
**Description:** Infra layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`, `repository.streak`, `orm.streak`
**Files:**
  - `streak_repo_impl.py` — `SQLAlchemyStreakRepository`

---

### Package: `service.streak`
**Layer:** service
**Path:** `src/service/streak`
**Description:** Service layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`, `repository.streak`, `dto.streak`, `service.student`, `service.nugget_wallet`
**Files:**
  - `streak_service.py` — `StreakService`, `StreakServiceImpl`

---

### Package: `api.streak`
**Layer:** api
**Path:** `src/api/streak`
**Description:** Api layer for the Streak domain class
**Tasks:** #112
**Depends on:** `service.streak`, `dto.streak`
**Files:**
  - `streak_router.py` — `StreakRouter`

---

### Package: `domain.reward_store`
**Layer:** domain
**Path:** `src/domain/reward_store`
**Description:** Domain layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** None
**Files:**
  - `RewardStore.py` — `RewardStore`, `RewardStoreId`, `RewardStoreCreatedEvent`, `RewardStoreUpdatedEvent`

---

### Package: `dto.reward_store`
**Layer:** dto
**Path:** `src/dto/reward_store`
**Description:** Dto layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_dto.py` — `RewardStoreCreateRequest`, `RewardStoreUpdateRequest`, `RewardStoreResponse`

---

### Package: `repository.reward_store`
**Layer:** repository
**Path:** `src/repository/reward_store`
**Description:** Repository layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_repository.py` — `RewardStoreRepository`

---

### Package: `orm.reward_store`
**Layer:** orm
**Path:** `src/orm/reward_store`
**Description:** Orm layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_orm.py` — `RewardStoreORM`

---

### Package: `infra.reward_store`
**Layer:** infra
**Path:** `src/infra/reward_store`
**Description:** Infra layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`, `repository.reward_store`, `orm.reward_store`
**Files:**
  - `reward_store_repo_impl.py` — `SQLAlchemyRewardStoreRepository`

---

### Package: `service.reward_store`
**Layer:** service
**Path:** `src/service/reward_store`
**Description:** Service layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`, `repository.reward_store`, `dto.reward_store`, `service.student`, `service.nugget_wallet`
**Files:**
  - `reward_store_service.py` — `RewardStoreService`, `RewardStoreServiceImpl`

---

### Package: `api.reward_store`
**Layer:** api
**Path:** `src/api/reward_store`
**Description:** Api layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `service.reward_store`, `dto.reward_store`
**Files:**
  - `reward_store_router.py` — `RewardStoreRouter`

---

### Package: `domain.reward_item`
**Layer:** domain
**Path:** `src/domain/reward_item`
**Description:** Domain layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** None
**Files:**
  - `RewardItem.py` — `RewardItem`, `RewardItemId`, `RewardItemCreatedEvent`, `RewardItemUpdatedEvent`

---

### Package: `dto.reward_item`
**Layer:** dto
**Path:** `src/dto/reward_item`
**Description:** Dto layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_dto.py` — `RewardItemCreateRequest`, `RewardItemUpdateRequest`, `RewardItemResponse`

---

### Package: `repository.reward_item`
**Layer:** repository
**Path:** `src/repository/reward_item`
**Description:** Repository layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_repository.py` — `RewardItemRepository`

---

### Package: `orm.reward_item`
**Layer:** orm
**Path:** `src/orm/reward_item`
**Description:** Orm layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_orm.py` — `RewardItemORM`

---

### Package: `infra.reward_item`
**Layer:** infra
**Path:** `src/infra/reward_item`
**Description:** Infra layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`, `repository.reward_item`, `orm.reward_item`
**Files:**
  - `reward_item_repo_impl.py` — `SQLAlchemyRewardItemRepository`

---

### Package: `service.reward_item`
**Layer:** service
**Path:** `src/service/reward_item`
**Description:** Service layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`, `repository.reward_item`, `dto.reward_item`, `service.student`, `service.nugget_wallet`
**Files:**
  - `reward_item_service.py` — `RewardItemService`, `RewardItemServiceImpl`

---

### Package: `api.reward_item`
**Layer:** api
**Path:** `src/api/reward_item`
**Description:** Api layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `service.reward_item`, `dto.reward_item`
**Files:**
  - `reward_item_router.py` — `RewardItemRouter`

---

### Package: `domain.redemption`
**Layer:** domain
**Path:** `src/domain/redemption`
**Description:** Domain layer for the Redemption domain class
**Tasks:** #114
**Depends on:** None
**Files:**
  - `Redemption.py` — `Redemption`, `RedemptionId`, `RedemptionCreatedEvent`, `RedemptionUpdatedEvent`

---

### Package: `dto.redemption`
**Layer:** dto
**Path:** `src/dto/redemption`
**Description:** Dto layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_dto.py` — `RedemptionCreateRequest`, `RedemptionUpdateRequest`, `RedemptionResponse`

---

### Package: `repository.redemption`
**Layer:** repository
**Path:** `src/repository/redemption`
**Description:** Repository layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_repository.py` — `RedemptionRepository`

---

### Package: `orm.redemption`
**Layer:** orm
**Path:** `src/orm/redemption`
**Description:** Orm layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_orm.py` — `RedemptionORM`

---

### Package: `infra.redemption`
**Layer:** infra
**Path:** `src/infra/redemption`
**Description:** Infra layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`, `repository.redemption`, `orm.redemption`
**Files:**
  - `redemption_repo_impl.py` — `SQLAlchemyRedemptionRepository`

---

### Package: `service.redemption`
**Layer:** service
**Path:** `src/service/redemption`
**Description:** Service layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`, `repository.redemption`, `dto.redemption`, `service.student`, `service.nugget_wallet`
**Files:**
  - `redemption_service.py` — `RedemptionService`, `RedemptionServiceImpl`

---

### Package: `api.redemption`
**Layer:** api
**Path:** `src/api/redemption`
**Description:** Api layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `service.redemption`, `dto.redemption`
**Files:**
  - `redemption_router.py` — `RedemptionRouter`

---

### Package: `domain.cohort_leaderboard`
**Layer:** domain
**Path:** `src/domain/cohort_leaderboard`
**Description:** Domain layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** None
**Files:**
  - `CohortLeaderboard.py` — `CohortLeaderboard`, `CohortLeaderboardId`, `CohortLeaderboardCreatedEvent`, `CohortLeaderboardUpdatedEvent`

---

### Package: `dto.cohort_leaderboard`
**Layer:** dto
**Path:** `src/dto/cohort_leaderboard`
**Description:** Dto layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_dto.py` — `CohortLeaderboardCreateRequest`, `CohortLeaderboardUpdateRequest`, `CohortLeaderboardResponse`

---

### Package: `repository.cohort_leaderboard`
**Layer:** repository
**Path:** `src/repository/cohort_leaderboard`
**Description:** Repository layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_repository.py` — `CohortLeaderboardRepository`

---

### Package: `orm.cohort_leaderboard`
**Layer:** orm
**Path:** `src/orm/cohort_leaderboard`
**Description:** Orm layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_orm.py` — `CohortLeaderboardORM`

---

### Package: `infra.cohort_leaderboard`
**Layer:** infra
**Path:** `src/infra/cohort_leaderboard`
**Description:** Infra layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `repository.cohort_leaderboard`, `orm.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_repo_impl.py` — `SQLAlchemyCohortLeaderboardRepository`

---

### Package: `service.cohort_leaderboard`
**Layer:** service
**Path:** `src/service/cohort_leaderboard`
**Description:** Service layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `repository.cohort_leaderboard`, `dto.cohort_leaderboard`, `service.student`, `service.nugget_wallet`, `service.cohort`
**Files:**
  - `cohort_leaderboard_service.py` — `CohortLeaderboardService`, `CohortLeaderboardServiceImpl`

---

### Package: `api.cohort_leaderboard`
**Layer:** api
**Path:** `src/api/cohort_leaderboard`
**Description:** Api layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `service.cohort_leaderboard`, `dto.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_router.py` — `CohortLeaderboardRouter`

---

### Package: `domain.instructor`
**Layer:** domain
**Path:** `src/domain/instructor`
**Description:** Domain layer for the Instructor domain class
**Tasks:** #105
**Depends on:** None
**Files:**
  - `Instructor.py` — `Instructor`, `InstructorId`, `InstructorCreatedEvent`, `InstructorUpdatedEvent`

---

### Package: `dto.instructor`
**Layer:** dto
**Path:** `src/dto/instructor`
**Description:** Dto layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_dto.py` — `InstructorCreateRequest`, `InstructorUpdateRequest`, `InstructorResponse`

---

### Package: `repository.instructor`
**Layer:** repository
**Path:** `src/repository/instructor`
**Description:** Repository layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_repository.py` — `InstructorRepository`

---

### Package: `orm.instructor`
**Layer:** orm
**Path:** `src/orm/instructor`
**Description:** Orm layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_orm.py` — `InstructorORM`

---

### Package: `infra.instructor`
**Layer:** infra
**Path:** `src/infra/instructor`
**Description:** Infra layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`, `repository.instructor`, `orm.instructor`
**Files:**
  - `instructor_repo_impl.py` — `SQLAlchemyInstructorRepository`

---

### Package: `service.instructor`
**Layer:** service
**Path:** `src/service/instructor`
**Description:** Service layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`, `repository.instructor`, `dto.instructor`, `service.competency`, `service.enrollment`
**Files:**
  - `instructor_service.py` — `InstructorService`, `InstructorServiceImpl`

---

### Package: `api.instructor`
**Layer:** api
**Path:** `src/api/instructor`
**Description:** Api layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `service.instructor`, `dto.instructor`
**Files:**
  - `instructor_router.py` — `InstructorRouter`

---

### Package: `domain.instructor_dashboard`
**Layer:** domain
**Path:** `src/domain/instructor_dashboard`
**Description:** Domain layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** None
**Files:**
  - `InstructorDashboard.py` — `InstructorDashboard`, `InstructorDashboardId`, `InstructorDashboardCreatedEvent`, `InstructorDashboardUpdatedEvent`

---

### Package: `dto.instructor_dashboard`
**Layer:** dto
**Path:** `src/dto/instructor_dashboard`
**Description:** Dto layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_dto.py` — `InstructorDashboardCreateRequest`, `InstructorDashboardUpdateRequest`, `InstructorDashboardResponse`

---

### Package: `repository.instructor_dashboard`
**Layer:** repository
**Path:** `src/repository/instructor_dashboard`
**Description:** Repository layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_repository.py` — `InstructorDashboardRepository`

---

### Package: `orm.instructor_dashboard`
**Layer:** orm
**Path:** `src/orm/instructor_dashboard`
**Description:** Orm layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_orm.py` — `InstructorDashboardORM`

---

### Package: `infra.instructor_dashboard`
**Layer:** infra
**Path:** `src/infra/instructor_dashboard`
**Description:** Infra layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `repository.instructor_dashboard`, `orm.instructor_dashboard`
**Files:**
  - `instructor_dashboard_repo_impl.py` — `SQLAlchemyInstructorDashboardRepository`

---

### Package: `service.instructor_dashboard`
**Layer:** service
**Path:** `src/service/instructor_dashboard`
**Description:** Service layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `repository.instructor_dashboard`, `dto.instructor_dashboard`, `service.competency`, `service.enrollment`
**Files:**
  - `instructor_dashboard_service.py` — `InstructorDashboardService`, `InstructorDashboardServiceImpl`

---

### Package: `api.instructor_dashboard`
**Layer:** api
**Path:** `src/api/instructor_dashboard`
**Description:** Api layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `service.instructor_dashboard`, `dto.instructor_dashboard`
**Files:**
  - `instructor_dashboard_router.py` — `InstructorDashboardRouter`

---

### Package: `domain.bonu_nugget_grant`
**Layer:** domain
**Path:** `src/domain/bonu_nugget_grant`
**Description:** Domain layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** None
**Files:**
  - `BonuNuggetGrant.py` — `BonuNuggetGrant`, `BonuNuggetGrantId`, `BonuNuggetGrantCreatedEvent`, `BonuNuggetGrantUpdatedEvent`

---

### Package: `dto.bonu_nugget_grant`
**Layer:** dto
**Path:** `src/dto/bonu_nugget_grant`
**Description:** Dto layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_dto.py` — `BonuNuggetGrantCreateRequest`, `BonuNuggetGrantUpdateRequest`, `BonuNuggetGrantResponse`

---

### Package: `repository.bonu_nugget_grant`
**Layer:** repository
**Path:** `src/repository/bonu_nugget_grant`
**Description:** Repository layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_repository.py` — `BonuNuggetGrantRepository`

---

### Package: `orm.bonu_nugget_grant`
**Layer:** orm
**Path:** `src/orm/bonu_nugget_grant`
**Description:** Orm layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_orm.py` — `BonuNuggetGrantORM`

---

### Package: `infra.bonu_nugget_grant`
**Layer:** infra
**Path:** `src/infra/bonu_nugget_grant`
**Description:** Infra layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `repository.bonu_nugget_grant`, `orm.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_repo_impl.py` — `SQLAlchemyBonuNuggetGrantRepository`

---

### Package: `service.bonu_nugget_grant`
**Layer:** service
**Path:** `src/service/bonu_nugget_grant`
**Description:** Service layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `repository.bonu_nugget_grant`, `dto.bonu_nugget_grant`, `service.student`, `service.nugget_wallet`, `service.instructor`
**Files:**
  - `bonu_nugget_grant_service.py` — `BonuNuggetGrantService`, `BonuNuggetGrantServiceImpl`

---

### Package: `api.bonu_nugget_grant`
**Layer:** api
**Path:** `src/api/bonu_nugget_grant`
**Description:** Api layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `service.bonu_nugget_grant`, `dto.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_router.py` — `BonuNuggetGrantRouter`

---

### Package: `domain.audit_event`
**Layer:** domain
**Path:** `src/domain/audit_event`
**Description:** Domain layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** None
**Files:**
  - `AuditEvent.py` — `AuditEvent`, `AuditEventId`, `AuditEventCreatedEvent`, `AuditEventUpdatedEvent`

---

### Package: `dto.audit_event`
**Layer:** dto
**Path:** `src/dto/audit_event`
**Description:** Dto layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_dto.py` — `AuditEventCreateRequest`, `AuditEventUpdateRequest`, `AuditEventResponse`

---

### Package: `repository.audit_event`
**Layer:** repository
**Path:** `src/repository/audit_event`
**Description:** Repository layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_repository.py` — `AuditEventRepository`

---

### Package: `orm.audit_event`
**Layer:** orm
**Path:** `src/orm/audit_event`
**Description:** Orm layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_orm.py` — `AuditEventORM`

---

### Package: `infra.audit_event`
**Layer:** infra
**Path:** `src/infra/audit_event`
**Description:** Infra layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`, `repository.audit_event`, `orm.audit_event`
**Files:**
  - `audit_event_repo_impl.py` — `SQLAlchemyAuditEventRepository`

---

### Package: `service.audit_event`
**Layer:** service
**Path:** `src/service/audit_event`
**Description:** Service layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`, `repository.audit_event`, `dto.audit_event`, `service.student`, `service.nugget_wallet`, `service.instructor`
**Files:**
  - `audit_event_service.py` — `AuditEventService`, `AuditEventServiceImpl`

---

### Package: `api.audit_event`
**Layer:** api
**Path:** `src/api/audit_event`
**Description:** Api layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `service.audit_event`, `dto.audit_event`
**Files:**
  - `audit_event_router.py` — `AuditEventRouter`

---

### Package: `tests.unit.exam_builder`
**Layer:** tests
**Path:** `tests/unit/exam_builder`
**Description:** Unit tests for ExamBuilder across domain, service, and API layers
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `service.exam_builder`, `api.exam_builder`
**Files:**
  - `test_exam_builder_domain.py`
  - `test_exam_builder_service.py`
  - `test_exam_builder_api.py`

---

### Package: `tests.unit.question`
**Layer:** tests
**Path:** `tests/unit/question`
**Description:** Unit tests for Question across domain, service, and API layers
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `service.question`, `api.question`
**Files:**
  - `test_question_domain.py`
  - `test_question_service.py`
  - `test_question_api.py`

---

### Package: `tests.unit.competency`
**Layer:** tests
**Path:** `tests/unit/competency`
**Description:** Unit tests for Competency across domain, service, and API layers
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `service.competency`, `api.competency`
**Files:**
  - `test_competency_domain.py`
  - `test_competency_service.py`
  - `test_competency_api.py`

---

### Package: `tests.unit.schedule`
**Layer:** tests
**Path:** `tests/unit/schedule`
**Description:** Unit tests for Schedule across domain, service, and API layers
**Tasks:** None
**Depends on:** `domain.schedule`, `service.schedule`, `api.schedule`
**Files:**
  - `test_schedule_domain.py`
  - `test_schedule_service.py`
  - `test_schedule_api.py`

---

### Package: `tests.unit.student`
**Layer:** tests
**Path:** `tests/unit/student`
**Description:** Unit tests for Student across domain, service, and API layers
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `service.student`, `api.student`
**Files:**
  - `test_student_domain.py`
  - `test_student_service.py`
  - `test_student_api.py`

---

### Package: `tests.unit.student_profile`
**Layer:** tests
**Path:** `tests/unit/student_profile`
**Description:** Unit tests for StudentProfile across domain, service, and API layers
**Tasks:** #110
**Depends on:** `domain.student_profile`, `service.student_profile`, `api.student_profile`
**Files:**
  - `test_student_profile_domain.py`
  - `test_student_profile_service.py`
  - `test_student_profile_api.py`

---

### Package: `tests.unit.nugget_wallet`
**Layer:** tests
**Path:** `tests/unit/nugget_wallet`
**Description:** Unit tests for NuggetWallet across domain, service, and API layers
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `service.nugget_wallet`, `api.nugget_wallet`
**Files:**
  - `test_nugget_wallet_domain.py`
  - `test_nugget_wallet_service.py`
  - `test_nugget_wallet_api.py`

---

### Package: `tests.unit.badge`
**Layer:** tests
**Path:** `tests/unit/badge`
**Description:** Unit tests for Badge across domain, service, and API layers
**Tasks:** #110
**Depends on:** `domain.badge`, `service.badge`, `api.badge`
**Files:**
  - `test_badge_domain.py`
  - `test_badge_service.py`
  - `test_badge_api.py`

---

### Package: `tests.unit.radar_chart`
**Layer:** tests
**Path:** `tests/unit/radar_chart`
**Description:** Unit tests for RadarChart across domain, service, and API layers
**Tasks:** None
**Depends on:** `domain.radar_chart`, `service.radar_chart`, `api.radar_chart`
**Files:**
  - `test_radar_chart_domain.py`
  - `test_radar_chart_service.py`
  - `test_radar_chart_api.py`

---

### Package: `tests.unit.competency_breakdown`
**Layer:** tests
**Path:** `tests/unit/competency_breakdown`
**Description:** Unit tests for CompetencyBreakdown across domain, service, and API layers
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `service.competency_breakdown`, `api.competency_breakdown`
**Files:**
  - `test_competency_breakdown_domain.py`
  - `test_competency_breakdown_service.py`
  - `test_competency_breakdown_api.py`

---

### Package: `tests.unit.study_tip`
**Layer:** tests
**Path:** `tests/unit/study_tip`
**Description:** Unit tests for StudyTip across domain, service, and API layers
**Tasks:** #113
**Depends on:** `domain.study_tip`, `service.study_tip`, `api.study_tip`
**Files:**
  - `test_study_tip_domain.py`
  - `test_study_tip_service.py`
  - `test_study_tip_api.py`

---

### Package: `tests.unit.cohort`
**Layer:** tests
**Path:** `tests/unit/cohort`
**Description:** Unit tests for Cohort across domain, service, and API layers
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `service.cohort`, `api.cohort`
**Files:**
  - `test_cohort_domain.py`
  - `test_cohort_service.py`
  - `test_cohort_api.py`

---

### Package: `tests.unit.enrollment`
**Layer:** tests
**Path:** `tests/unit/enrollment`
**Description:** Unit tests for Enrollment across domain, service, and API layers
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `service.enrollment`, `api.enrollment`
**Files:**
  - `test_enrollment_domain.py`
  - `test_enrollment_service.py`
  - `test_enrollment_api.py`

---

### Package: `tests.unit.attempt_review`
**Layer:** tests
**Path:** `tests/unit/attempt_review`
**Description:** Unit tests for AttemptReview across domain, service, and API layers
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `service.attempt_review`, `api.attempt_review`
**Files:**
  - `test_attempt_review_domain.py`
  - `test_attempt_review_service.py`
  - `test_attempt_review_api.py`

---

### Package: `tests.unit.competency_trend_chart`
**Layer:** tests
**Path:** `tests/unit/competency_trend_chart`
**Description:** Unit tests for CompetencyTrendChart across domain, service, and API layers
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`, `service.competency_trend_chart`, `api.competency_trend_chart`
**Files:**
  - `test_competency_trend_chart_domain.py`
  - `test_competency_trend_chart_service.py`
  - `test_competency_trend_chart_api.py`

---

### Package: `tests.unit.exam_session`
**Layer:** tests
**Path:** `tests/unit/exam_session`
**Description:** Unit tests for ExamSession across domain, service, and API layers
**Tasks:** #111
**Depends on:** `domain.exam_session`, `service.exam_session`, `api.exam_session`
**Files:**
  - `test_exam_session_domain.py`
  - `test_exam_session_service.py`
  - `test_exam_session_api.py`

---

### Package: `tests.unit.streak`
**Layer:** tests
**Path:** `tests/unit/streak`
**Description:** Unit tests for Streak across domain, service, and API layers
**Tasks:** #112
**Depends on:** `domain.streak`, `service.streak`, `api.streak`
**Files:**
  - `test_streak_domain.py`
  - `test_streak_service.py`
  - `test_streak_api.py`

---

### Package: `tests.unit.reward_store`
**Layer:** tests
**Path:** `tests/unit/reward_store`
**Description:** Unit tests for RewardStore across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.reward_store`, `service.reward_store`, `api.reward_store`
**Files:**
  - `test_reward_store_domain.py`
  - `test_reward_store_service.py`
  - `test_reward_store_api.py`

---

### Package: `tests.unit.reward_item`
**Layer:** tests
**Path:** `tests/unit/reward_item`
**Description:** Unit tests for RewardItem across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.reward_item`, `service.reward_item`, `api.reward_item`
**Files:**
  - `test_reward_item_domain.py`
  - `test_reward_item_service.py`
  - `test_reward_item_api.py`

---

### Package: `tests.unit.redemption`
**Layer:** tests
**Path:** `tests/unit/redemption`
**Description:** Unit tests for Redemption across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.redemption`, `service.redemption`, `api.redemption`
**Files:**
  - `test_redemption_domain.py`
  - `test_redemption_service.py`
  - `test_redemption_api.py`

---

### Package: `tests.unit.cohort_leaderboard`
**Layer:** tests
**Path:** `tests/unit/cohort_leaderboard`
**Description:** Unit tests for CohortLeaderboard across domain, service, and API layers
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `service.cohort_leaderboard`, `api.cohort_leaderboard`
**Files:**
  - `test_cohort_leaderboard_domain.py`
  - `test_cohort_leaderboard_service.py`
  - `test_cohort_leaderboard_api.py`

---

### Package: `tests.unit.instructor`
**Layer:** tests
**Path:** `tests/unit/instructor`
**Description:** Unit tests for Instructor across domain, service, and API layers
**Tasks:** #105
**Depends on:** `domain.instructor`, `service.instructor`, `api.instructor`
**Files:**
  - `test_instructor_domain.py`
  - `test_instructor_service.py`
  - `test_instructor_api.py`

---

### Package: `tests.unit.instructor_dashboard`
**Layer:** tests
**Path:** `tests/unit/instructor_dashboard`
**Description:** Unit tests for InstructorDashboard across domain, service, and API layers
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `service.instructor_dashboard`, `api.instructor_dashboard`
**Files:**
  - `test_instructor_dashboard_domain.py`
  - `test_instructor_dashboard_service.py`
  - `test_instructor_dashboard_api.py`

---

### Package: `tests.unit.bonu_nugget_grant`
**Layer:** tests
**Path:** `tests/unit/bonu_nugget_grant`
**Description:** Unit tests for BonuNuggetGrant across domain, service, and API layers
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `service.bonu_nugget_grant`, `api.bonu_nugget_grant`
**Files:**
  - `test_bonu_nugget_grant_domain.py`
  - `test_bonu_nugget_grant_service.py`
  - `test_bonu_nugget_grant_api.py`

---

### Package: `tests.unit.audit_event`
**Layer:** tests
**Path:** `tests/unit/audit_event`
**Description:** Unit tests for AuditEvent across domain, service, and API layers
**Tasks:** #109
**Depends on:** `domain.audit_event`, `service.audit_event`, `api.audit_event`
**Files:**
  - `test_audit_event_domain.py`
  - `test_audit_event_service.py`
  - `test_audit_event_api.py`

---

### Package: `tests.integration`
**Layer:** tests
**Path:** `tests/integration`
**Description:** End-to-end and cross-service integration tests
**Tasks:** None
**Depends on:** `api.exam_builder`, `api.question`, `api.competency`, `api.schedule`, `api.student`, `api.student_profile`, `api.nugget_wallet`, `api.badge`, `api.radar_chart`, `api.competency_breakdown`, `api.study_tip`, `api.cohort`, `api.enrollment`, `api.attempt_review`, `api.competency_trend_chart`, `api.exam_session`, `api.streak`, `api.reward_store`, `api.reward_item`, `api.redemption`, `api.cohort_leaderboard`, `api.instructor`, `api.instructor_dashboard`, `api.bonu_nugget_grant`, `api.audit_event`
**Files:**
  - `test_exam_builder_flow.py`
  - `test_question_flow.py`
  - `test_competency_flow.py`
  - `test_schedule_flow.py`
  - `test_student_flow.py`
  - `test_student_profile_flow.py`
  - `test_nugget_wallet_flow.py`
  - `test_badge_flow.py`
  - `test_radar_chart_flow.py`
  - `test_competency_breakdown_flow.py`
  - `test_study_tip_flow.py`
  - `test_cohort_flow.py`
  - `test_enrollment_flow.py`
  - `test_attempt_review_flow.py`
  - `test_competency_trend_chart_flow.py`
  - `test_exam_session_flow.py`
  - `test_streak_flow.py`
  - `test_reward_store_flow.py`
  - `test_reward_item_flow.py`
  - `test_redemption_flow.py`
  - `test_cohort_leaderboard_flow.py`
  - `test_instructor_flow.py`
  - `test_instructor_dashboard_flow.py`
  - `test_bonu_nugget_grant_flow.py`
  - `test_audit_event_flow.py`
  - `test_api_contracts.py`
  - `conftest.py`

---

### Package: `config.settings`
**Layer:** config
**Path:** `src/config`
**Description:** Application settings, environment variables, dependency injection
**Tasks:** None
**Depends on:** None
**Files:**
  - `settings.py` — `Settings`
  - `dependencies.py` — `Container`
  - `database.py`
  - `logging.py`

---

### Package: `docs.api_and_deployment`
**Layer:** docs
**Path:** `docs`
**Description:** OpenAPI documentation, admin guide, multi-city config, deployment runbook
**Tasks:** None
**Depends on:** None
**Files:**
  - `openapi.md`
  - `deployment_guide.md`
  - `multi_city_config.md`
  - `monitoring.md`

---

### Package: `domain.badge`
**Layer:** domain
**Path:** `src/domain/badge`
**Description:** Domain layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `Badge.py` — `StudentAccount`, `RegistrationData`, `Avatar`, `Badge`, `BadgeId`, `BadgeCreatedEvent`, `BadgeUpdatedEvent`

---

### Package: `dto.badge`
**Layer:** dto
**Path:** `src/dto/badge`
**Description:** Dto layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_dto.py` — `BadgeCreateRequest`, `BadgeUpdateRequest`, `BadgeResponse`

---

### Package: `repository.badge`
**Layer:** repository
**Path:** `src/repository/badge`
**Description:** Repository layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_repository.py` — `BadgeRepository`

---

### Package: `orm.badge`
**Layer:** orm
**Path:** `src/orm/badge`
**Description:** Orm layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`
**Files:**
  - `badge_orm.py` — `BadgeORM`

---

### Package: `infra.badge`
**Layer:** infra
**Path:** `src/infra/badge`
**Description:** Infra layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`, `orm.badge`, `repository.badge`
**Files:**
  - `badge_repo_impl.py` — `SQLAlchemyBadgeRepository`

---

### Package: `service.badge`
**Layer:** service
**Path:** `src/service/badge`
**Description:** Service layer for the Badge domain class
**Tasks:** #110
**Depends on:** `domain.badge`, `domain.student_profile`, `dto.badge`, `repository.badge`
**Files:**
  - `badge_service.py` — `RegistrationService`, `RegistrationInput`

---

### Package: `api.badge`
**Layer:** api
**Path:** `src/api/badge`
**Description:** Api layer for the Badge domain class
**Tasks:** #110
**Depends on:** `dto.badge`, `service.badge`, `service.student_profile`
**Files:**
  - `badge_router.py` — `RegistrationController`

---

### Package: `tests.unit.badge`
**Layer:** tests
**Path:** `tests/unit/badge`
**Description:** Unit tests for Badge across domain, service, and API layers
**Tasks:** #110
**Depends on:** `domain.badge`, `service.badge`, `api.badge`
**Files:**
  - `test_badge_domain.py`
  - `test_badge_service.py`
  - `test_badge_api.py`

---

### Package: `domain.competency`
**Layer:** domain
**Path:** `src/domain/competency`
**Description:** Domain layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.question`, `domain.study_tip`
**Files:**
  - `Competency.py` — `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `Competency`, `DifficultyTag`, `CompetencyId`, `CompetencyCreatedEvent`, `CompetencyUpdatedEvent`

---

### Package: `dto.competency`
**Layer:** dto
**Path:** `src/dto/competency`
**Description:** Dto layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `domain.question`
**Files:**
  - `competency_dto.py` — `CreateQuestionRequest`, `CreateQuestionResponse`

---

### Package: `repository.competency`
**Layer:** repository
**Path:** `src/repository/competency`
**Description:** Repository layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`
**Files:**
  - `competency_repository.py` — `QuestionCreationAPI`, `ExamBuilderDatabase`

---

### Package: `orm.competency`
**Layer:** orm
**Path:** `src/orm/competency`
**Description:** Orm layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`
**Files:**
  - `competency_orm.py` — `CompetencyORM`

---

### Package: `infra.competency`
**Layer:** infra
**Path:** `src/infra/competency`
**Description:** Infra layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `orm.competency`, `repository.competency`
**Files:**
  - `competency_repo_impl.py` — `SQLAlchemyCompetencyRepository`

---

### Package: `service.competency`
**Layer:** service
**Path:** `src/service/competency`
**Description:** Service layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `domain.study_tip`, `dto.competency`, `repository.competency`
**Files:**
  - `competency_service.py` — `Operation`

---

### Package: `api.competency`
**Layer:** api
**Path:** `src/api/competency`
**Description:** Api layer for the Competency domain class
**Tasks:** #105, #106, #113, #116
**Depends on:** `dto.competency`, `service.competency`
**Files:**
  - `competency_router.py` — `CompetencyRouter`

---

### Package: `tests.unit.competency`
**Layer:** tests
**Path:** `tests/unit/competency`
**Description:** Unit tests for Competency across domain, service, and API layers
**Tasks:** #105, #106, #113, #116
**Depends on:** `domain.competency`, `service.competency`, `api.competency`
**Files:**
  - `test_competency_domain.py`
  - `test_competency_service.py`
  - `test_competency_api.py`

---

### Package: `domain.competency_breakdown`
**Layer:** domain
**Path:** `src/domain/competency_breakdown`
**Description:** Domain layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency`, `domain.instructor`
**Files:**
  - `CompetencyBreakdown.py` — `Actor`, `Students`, `Academic_Advisors`, `Instructors`, `Resource`, `StudentDashboardResource`, `ExamAnalysisAPIResource`, `Permission`, `State`, `CompetencyBreakdown`, `CompetencyBreakdownId`, `CompetencyBreakdownCreatedEvent`, `CompetencyBreakdownUpdatedEvent`

---

### Package: `dto.competency_breakdown`
**Layer:** dto
**Path:** `src/dto/competency_breakdown`
**Description:** Dto layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`
**Files:**
  - `competency_breakdown_dto.py` — `CompetencyBreakdownCreateRequest`, `CompetencyBreakdownUpdateRequest`, `CompetencyBreakdownResponse`

---

### Package: `repository.competency_breakdown`
**Layer:** repository
**Path:** `src/repository/competency_breakdown`
**Description:** Repository layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `repository.streak`
**Files:**
  - `competency_breakdown_repository.py` — `Interface`, `Exam_Analysis_API`, `Student_Dashboard`

---

### Package: `orm.competency_breakdown`
**Layer:** orm
**Path:** `src/orm/competency_breakdown`
**Description:** Orm layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`
**Files:**
  - `competency_breakdown_orm.py` — `CompetencyBreakdownORM`

---

### Package: `infra.competency_breakdown`
**Layer:** infra
**Path:** `src/infra/competency_breakdown`
**Description:** Infra layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `orm.competency_breakdown`, `repository.competency_breakdown`
**Files:**
  - `competency_breakdown_repo_impl.py` — `SQLAlchemyCompetencyBreakdownRepository`

---

### Package: `service.competency_breakdown`
**Layer:** service
**Path:** `src/service/competency_breakdown`
**Description:** Service layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `domain.study_tip`, `dto.competency_breakdown`, `repository.competency_breakdown`, `service.competency`
**Files:**
  - `competency_breakdown_service.py` — `REQ_EDU_01`

---

### Package: `api.competency_breakdown`
**Layer:** api
**Path:** `src/api/competency_breakdown`
**Description:** Api layer for the CompetencyBreakdown domain class
**Tasks:** #113
**Depends on:** `dto.competency_breakdown`, `service.competency_breakdown`
**Files:**
  - `competency_breakdown_router.py` — `CompetencyBreakdownRouter`

---

### Package: `tests.unit.competency_breakdown`
**Layer:** tests
**Path:** `tests/unit/competency_breakdown`
**Description:** Unit tests for CompetencyBreakdown across domain, service, and API layers
**Tasks:** #113
**Depends on:** `domain.competency_breakdown`, `service.competency_breakdown`, `api.competency_breakdown`
**Files:**
  - `test_competency_breakdown_domain.py`
  - `test_competency_breakdown_service.py`
  - `test_competency_breakdown_api.py`

---

### Package: `domain.exam_builder`
**Layer:** domain
**Path:** `src/domain/exam_builder`
**Description:** Domain layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.study_tip`
**Files:**
  - `ExamBuilder.py` — `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `DifficultyTag`, `ExamBuilder`, `ExamBuilderId`, `ExamBuilderCreatedEvent`, `ExamBuilderUpdatedEvent`

---

### Package: `dto.exam_builder`
**Layer:** dto
**Path:** `src/dto/exam_builder`
**Description:** Dto layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `domain.question`
**Files:**
  - `exam_builder_dto.py` — `CreateQuestionRequest`, `CreateQuestionResponse`

---

### Package: `repository.exam_builder`
**Layer:** repository
**Path:** `src/repository/exam_builder`
**Description:** Repository layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`
**Files:**
  - `exam_builder_repository.py` — `QuestionCreationAPI`, `ExamBuilderDatabase`

---

### Package: `orm.exam_builder`
**Layer:** orm
**Path:** `src/orm/exam_builder`
**Description:** Orm layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`
**Files:**
  - `exam_builder_orm.py` — `ExamBuilderORM`

---

### Package: `infra.exam_builder`
**Layer:** infra
**Path:** `src/infra/exam_builder`
**Description:** Infra layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `orm.exam_builder`, `repository.exam_builder`
**Files:**
  - `exam_builder_repo_impl.py` — `SQLAlchemyExamBuilderRepository`

---

### Package: `service.exam_builder`
**Layer:** service
**Path:** `src/service/exam_builder`
**Description:** Service layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `domain.study_tip`, `dto.exam_builder`, `repository.exam_builder`
**Files:**
  - `exam_builder_service.py` — `Operation`

---

### Package: `api.exam_builder`
**Layer:** api
**Path:** `src/api/exam_builder`
**Description:** Api layer for the ExamBuilder domain class
**Tasks:** #106
**Depends on:** `dto.exam_builder`, `service.exam_builder`
**Files:**
  - `exam_builder_router.py` — `ExamBuilderRouter`

---

### Package: `tests.unit.exam_builder`
**Layer:** tests
**Path:** `tests/unit/exam_builder`
**Description:** Unit tests for ExamBuilder across domain, service, and API layers
**Tasks:** #106
**Depends on:** `domain.exam_builder`, `service.exam_builder`, `api.exam_builder`
**Files:**
  - `test_exam_builder_domain.py`
  - `test_exam_builder_service.py`
  - `test_exam_builder_api.py`

---

### Package: `domain.nugget_wallet`
**Layer:** domain
**Path:** `src/domain/nugget_wallet`
**Description:** Domain layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.streak`, `domain.student`, `domain.student_profile`
**Files:**
  - `NuggetWallet.py` — `StudentAccount`, `RegistrationData`, `Avatar`, `NuggetWallet`, `NuggetWalletId`, `NuggetWalletCreatedEvent`, `NuggetWalletUpdatedEvent`

---

### Package: `dto.nugget_wallet`
**Layer:** dto
**Path:** `src/dto/nugget_wallet`
**Description:** Dto layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_dto.py` — `NuggetWalletCreateRequest`, `NuggetWalletUpdateRequest`, `NuggetWalletResponse`

---

### Package: `repository.nugget_wallet`
**Layer:** repository
**Path:** `src/repository/nugget_wallet`
**Description:** Repository layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_repository.py` — `NuggetWalletRepository`

---

### Package: `orm.nugget_wallet`
**Layer:** orm
**Path:** `src/orm/nugget_wallet`
**Description:** Orm layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`
**Files:**
  - `nugget_wallet_orm.py` — `NuggetWalletORM`

---

### Package: `infra.nugget_wallet`
**Layer:** infra
**Path:** `src/infra/nugget_wallet`
**Description:** Infra layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `orm.nugget_wallet`, `repository.nugget_wallet`
**Files:**
  - `nugget_wallet_repo_impl.py` — `SQLAlchemyNuggetWalletRepository`

---

### Package: `service.nugget_wallet`
**Layer:** service
**Path:** `src/service/nugget_wallet`
**Description:** Service layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `domain.student_profile`, `dto.nugget_wallet`, `repository.nugget_wallet`
**Files:**
  - `nugget_wallet_service.py` — `RegistrationService`, `RegistrationInput`

---

### Package: `api.nugget_wallet`
**Layer:** api
**Path:** `src/api/nugget_wallet`
**Description:** Api layer for the NuggetWallet domain class
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `dto.nugget_wallet`, `service.nugget_wallet`, `service.student_profile`
**Files:**
  - `nugget_wallet_router.py` — `RegistrationController`

---

### Package: `tests.unit.nugget_wallet`
**Layer:** tests
**Path:** `tests/unit/nugget_wallet`
**Description:** Unit tests for NuggetWallet across domain, service, and API layers
**Tasks:** #109, #110, #111, #112, #114, #115
**Depends on:** `domain.nugget_wallet`, `service.nugget_wallet`, `api.nugget_wallet`
**Files:**
  - `test_nugget_wallet_domain.py`
  - `test_nugget_wallet_service.py`
  - `test_nugget_wallet_api.py`

---

### Package: `domain.question`
**Layer:** domain
**Path:** `src/domain/question`
**Description:** Domain layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.competency`, `domain.study_tip`
**Files:**
  - `Question.py` — `QuestionType`, `DifficultyTier`, `Permission`, `State`, `Resource`, `DifficultyTag`, `Question`, `QuestionId`, `QuestionCreatedEvent`, `QuestionUpdatedEvent`

---

### Package: `dto.question`
**Layer:** dto
**Path:** `src/dto/question`
**Description:** Dto layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_dto.py` — `CreateQuestionRequest`, `CreateQuestionResponse`

---

### Package: `repository.question`
**Layer:** repository
**Path:** `src/repository/question`
**Description:** Repository layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_repository.py` — `QuestionCreationAPI`, `ExamBuilderDatabase`

---

### Package: `orm.question`
**Layer:** orm
**Path:** `src/orm/question`
**Description:** Orm layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`
**Files:**
  - `question_orm.py` — `QuestionORM`

---

### Package: `infra.question`
**Layer:** infra
**Path:** `src/infra/question`
**Description:** Infra layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `orm.question`, `repository.question`
**Files:**
  - `question_repo_impl.py` — `SQLAlchemyQuestionRepository`

---

### Package: `service.question`
**Layer:** service
**Path:** `src/service/question`
**Description:** Service layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `domain.study_tip`, `dto.question`, `repository.question`
**Files:**
  - `question_service.py` — `Operation`

---

### Package: `api.question`
**Layer:** api
**Path:** `src/api/question`
**Description:** Api layer for the Question domain class
**Tasks:** #106, #111, #116
**Depends on:** `dto.question`, `service.question`
**Files:**
  - `question_router.py` — `QuestionRouter`

---

### Package: `tests.unit.question`
**Layer:** tests
**Path:** `tests/unit/question`
**Description:** Unit tests for Question across domain, service, and API layers
**Tasks:** #106, #111, #116
**Depends on:** `domain.question`, `service.question`, `api.question`
**Files:**
  - `test_question_domain.py`
  - `test_question_service.py`
  - `test_question_api.py`

---

### Package: `domain.radar_chart`
**Layer:** domain
**Path:** `src/domain/radar_chart`
**Description:** Domain layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.student_profile`
**Files:**
  - `RadarChart.py` — `RadarChart`, `RadarChartId`, `RadarChartCreatedEvent`, `RadarChartUpdatedEvent`

---

### Package: `dto.radar_chart`
**Layer:** dto
**Path:** `src/dto/radar_chart`
**Description:** Dto layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_dto.py` — `RadarChartCreateRequest`, `RadarChartUpdateRequest`, `RadarChartResponse`

---

### Package: `repository.radar_chart`
**Layer:** repository
**Path:** `src/repository/radar_chart`
**Description:** Repository layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_repository.py` — `RadarChartRepository`

---

### Package: `orm.radar_chart`
**Layer:** orm
**Path:** `src/orm/radar_chart`
**Description:** Orm layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`
**Files:**
  - `radar_chart_orm.py` — `RadarChartORM`

---

### Package: `infra.radar_chart`
**Layer:** infra
**Path:** `src/infra/radar_chart`
**Description:** Infra layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`, `orm.radar_chart`, `repository.radar_chart`
**Files:**
  - `radar_chart_repo_impl.py` — `SQLAlchemyRadarChartRepository`

---

### Package: `service.radar_chart`
**Layer:** service
**Path:** `src/service/radar_chart`
**Description:** Service layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `domain.radar_chart`, `dto.radar_chart`, `repository.radar_chart`
**Files:**
  - `radar_chart_service.py` — `RadarChartService`, `RadarChartServiceImpl`

---

### Package: `api.radar_chart`
**Layer:** api
**Path:** `src/api/radar_chart`
**Description:** Api layer for the RadarChart domain class
**Tasks:** None
**Depends on:** `dto.radar_chart`, `service.radar_chart`
**Files:**
  - `radar_chart_router.py` — `RadarChartRouter`

---

### Package: `tests.unit.radar_chart`
**Layer:** tests
**Path:** `tests/unit/radar_chart`
**Description:** Unit tests for RadarChart across domain, service, and API layers
**Tasks:** None
**Depends on:** `domain.radar_chart`, `service.radar_chart`, `api.radar_chart`
**Files:**
  - `test_radar_chart_domain.py`
  - `test_radar_chart_service.py`
  - `test_radar_chart_api.py`

---

### Package: `domain.schedule`
**Layer:** domain
**Path:** `src/domain/schedule`
**Description:** Domain layer for the Schedule domain class
**Tasks:** None
**Depends on:** None
**Files:**
  - `Schedule.py` — `Schedule`, `ScheduleId`, `ScheduleCreatedEvent`, `ScheduleUpdatedEvent`

---

### Package: `dto.schedule`
**Layer:** dto
**Path:** `src/dto/schedule`
**Description:** Dto layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_dto.py` — `ScheduleCreateRequest`, `ScheduleUpdateRequest`, `ScheduleResponse`

---

### Package: `repository.schedule`
**Layer:** repository
**Path:** `src/repository/schedule`
**Description:** Repository layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_repository.py` — `ScheduleRepository`

---

### Package: `orm.schedule`
**Layer:** orm
**Path:** `src/orm/schedule`
**Description:** Orm layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`
**Files:**
  - `schedule_orm.py` — `ScheduleORM`

---

### Package: `infra.schedule`
**Layer:** infra
**Path:** `src/infra/schedule`
**Description:** Infra layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`, `orm.schedule`, `repository.schedule`
**Files:**
  - `schedule_repo_impl.py` — `SQLAlchemyScheduleRepository`

---

### Package: `service.schedule`
**Layer:** service
**Path:** `src/service/schedule`
**Description:** Service layer for the Schedule domain class
**Tasks:** None
**Depends on:** `domain.schedule`, `dto.schedule`, `repository.schedule`
**Files:**
  - `schedule_service.py` — `ScheduleService`, `ScheduleServiceImpl`

---

### Package: `api.schedule`
**Layer:** api
**Path:** `src/api/schedule`
**Description:** Api layer for the Schedule domain class
**Tasks:** None
**Depends on:** `dto.schedule`, `service.schedule`
**Files:**
  - `schedule_router.py` — `ScheduleRouter`

---

### Package: `tests.unit.schedule`
**Layer:** tests
**Path:** `tests/unit/schedule`
**Description:** Unit tests for Schedule across domain, service, and API layers
**Tasks:** None
**Depends on:** `domain.schedule`, `service.schedule`, `api.schedule`
**Files:**
  - `test_schedule_domain.py`
  - `test_schedule_service.py`
  - `test_schedule_api.py`

---

### Package: `domain.student`
**Layer:** domain
**Path:** `src/domain/student`
**Description:** Domain layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.cohort`, `domain.competency`, `domain.exam_session`, `domain.nugget_wallet`, `domain.student_profile`, `domain.study_tip`, `service.competency_trend_chart`
**Files:**
  - `Student.py` — `StudentAccount`, `RegistrationData`, `Avatar`, `Student`, `StudentId`, `StudentCreatedEvent`, `StudentUpdatedEvent`

---

### Package: `dto.student`
**Layer:** dto
**Path:** `src/dto/student`
**Description:** Dto layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_dto.py` — `StudentCreateRequest`, `StudentUpdateRequest`, `StudentResponse`

---

### Package: `repository.student`
**Layer:** repository
**Path:** `src/repository/student`
**Description:** Repository layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_repository.py` — `StudentRepository`

---

### Package: `orm.student`
**Layer:** orm
**Path:** `src/orm/student`
**Description:** Orm layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`
**Files:**
  - `student_orm.py` — `StudentORM`

---

### Package: `infra.student`
**Layer:** infra
**Path:** `src/infra/student`
**Description:** Infra layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `orm.student`, `repository.student`
**Files:**
  - `student_repo_impl.py` — `SQLAlchemyStudentRepository`

---

### Package: `service.student`
**Layer:** service
**Path:** `src/service/student`
**Description:** Service layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `domain.student_profile`, `dto.student`, `repository.student`
**Files:**
  - `student_service.py` — `RegistrationService`, `RegistrationInput`

---

### Package: `api.student`
**Layer:** api
**Path:** `src/api/student`
**Description:** Api layer for the Student domain class
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `dto.student`, `service.student`, `service.student_profile`
**Files:**
  - `student_router.py` — `RegistrationController`

---

### Package: `tests.unit.student`
**Layer:** tests
**Path:** `tests/unit/student`
**Description:** Unit tests for Student across domain, service, and API layers
**Tasks:** #108, #109, #110, #111, #112, #114, #115, #116
**Depends on:** `domain.student`, `service.student`, `api.student`
**Files:**
  - `test_student_domain.py`
  - `test_student_service.py`
  - `test_student_api.py`

---

### Package: `domain.attempt_review`
**Layer:** domain
**Path:** `src/domain/attempt_review`
**Description:** Domain layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.competency`, `domain.question`, `domain.student`
**Files:**
  - `AttemptReview.py` — `Attempt`, `ChartPoint`, `AttemptReview`, `AttemptReviewId`, `AttemptReviewCreatedEvent`, `AttemptReviewUpdatedEvent`

---

### Package: `dto.attempt_review`
**Layer:** dto
**Path:** `src/dto/attempt_review`
**Description:** Dto layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`
**Files:**
  - `attempt_review_dto.py` — `AttemptReviewCreateRequest`, `AttemptReviewUpdateRequest`, `AttemptReviewResponse`

---

### Package: `repository.attempt_review`
**Layer:** repository
**Path:** `src/repository/attempt_review`
**Description:** Repository layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `domain.competency`, `domain.competency_trend_chart`, `service.competency_trend_chart`
**Files:**
  - `attempt_review_repository.py` — `StudentDashboardUI`, `StudentDataAPI`, `TrendAPI`, `StudentDataStore`

---

### Package: `orm.attempt_review`
**Layer:** orm
**Path:** `src/orm/attempt_review`
**Description:** Orm layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`
**Files:**
  - `attempt_review_orm.py` — `AttemptReviewORM`

---

### Package: `infra.attempt_review`
**Layer:** infra
**Path:** `src/infra/attempt_review`
**Description:** Infra layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `orm.attempt_review`, `repository.attempt_review`
**Files:**
  - `attempt_review_repo_impl.py` — `SQLAlchemyAttemptReviewRepository`

---

### Package: `service.attempt_review`
**Layer:** service
**Path:** `src/service/attempt_review`
**Description:** Service layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `domain.competency`, `domain.competency_trend_chart`, `domain.student`, `domain.study_tip`, `dto.attempt_review`, `repository.attempt_review`, `repository.competency_trend_chart`, `service.competency`, `service.question`, `service.student`
**Files:**
  - `attempt_review_service.py` — `PastAttemptData`, `DashboardData`, `TrendData`, `ReviewService`, `AccessControlService`, `Permission`, `Role`

---

### Package: `api.attempt_review`
**Layer:** api
**Path:** `src/api/attempt_review`
**Description:** Api layer for the AttemptReview domain class
**Tasks:** #116
**Depends on:** `dto.attempt_review`, `service.attempt_review`, `service.competency_trend_chart`
**Files:**
  - `attempt_review_router.py` — `ReviewController`

---

### Package: `tests.unit.attempt_review`
**Layer:** tests
**Path:** `tests/unit/attempt_review`
**Description:** Unit tests for AttemptReview across domain, service, and API layers
**Tasks:** #116
**Depends on:** `domain.attempt_review`, `service.attempt_review`, `api.attempt_review`
**Files:**
  - `test_attempt_review_domain.py`
  - `test_attempt_review_service.py`
  - `test_attempt_review_api.py`

---

### Package: `domain.cohort`
**Layer:** domain
**Path:** `src/domain/cohort`
**Description:** Domain layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.student`, `domain.study_tip`
**Files:**
  - `Cohort.py` — `Cohort`, `Exam`, `Administrator`, `IT_Team`, `CohortId`, `CohortCreatedEvent`, `CohortUpdatedEvent`

---

### Package: `dto.cohort`
**Layer:** dto
**Path:** `src/dto/cohort`
**Description:** Dto layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_dto.py` — `CohortCreateRequest`, `CohortUpdateRequest`, `CohortResponse`

---

### Package: `repository.cohort`
**Layer:** repository
**Path:** `src/repository/cohort`
**Description:** Repository layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_repository.py` — `CohortRepository`

---

### Package: `orm.cohort`
**Layer:** orm
**Path:** `src/orm/cohort`
**Description:** Orm layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`
**Files:**
  - `cohort_orm.py` — `CohortORM`

---

### Package: `infra.cohort`
**Layer:** infra
**Path:** `src/infra/cohort`
**Description:** Infra layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `orm.cohort`, `repository.cohort`
**Files:**
  - `cohort_repo_impl.py` — `SQLAlchemyCohortRepository`

---

### Package: `service.cohort`
**Layer:** service
**Path:** `src/service/cohort`
**Description:** Service layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `domain.student`, `dto.cohort`, `repository.cohort`, `service.student`
**Files:**
  - `cohort_service.py` — `CohortService`, `CohortServiceImpl`

---

### Package: `api.cohort`
**Layer:** api
**Path:** `src/api/cohort`
**Description:** Api layer for the Cohort domain class
**Tasks:** #108, #115
**Depends on:** `dto.cohort`, `service.cohort`
**Files:**
  - `cohort_router.py` — `CohortRouter`

---

### Package: `tests.unit.cohort`
**Layer:** tests
**Path:** `tests/unit/cohort`
**Description:** Unit tests for Cohort across domain, service, and API layers
**Tasks:** #108, #115
**Depends on:** `domain.cohort`, `service.cohort`, `api.cohort`
**Files:**
  - `test_cohort_domain.py`
  - `test_cohort_service.py`
  - `test_cohort_api.py`

---

### Package: `domain.cohort_leaderboard`
**Layer:** domain
**Path:** `src/domain/cohort_leaderboard`
**Description:** Domain layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort`, `domain.instructor`, `domain.nugget_wallet`, `domain.student`, `repository.streak`
**Files:**
  - `CohortLeaderboard.py` — `Actor`, `Resource`, `Interface`, `Permission`, `State`, `CohortLeaderboard`, `CohortLeaderboardId`, `CohortLeaderboardCreatedEvent`, `CohortLeaderboardUpdatedEvent`

---

### Package: `dto.cohort_leaderboard`
**Layer:** dto
**Path:** `src/dto/cohort_leaderboard`
**Description:** Dto layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_dto.py` — `CohortLeaderboardCreateRequest`, `CohortLeaderboardUpdateRequest`, `CohortLeaderboardResponse`

---

### Package: `repository.cohort_leaderboard`
**Layer:** repository
**Path:** `src/repository/cohort_leaderboard`
**Description:** Repository layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `repository.streak`
**Files:**
  - `cohort_leaderboard_repository.py` — `Student_Data_Store`, `Cohort_Settings_API`, `Leaderboard_Display`

---

### Package: `orm.cohort_leaderboard`
**Layer:** orm
**Path:** `src/orm/cohort_leaderboard`
**Description:** Orm layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_orm.py` — `CohortLeaderboardORM`

---

### Package: `infra.cohort_leaderboard`
**Layer:** infra
**Path:** `src/infra/cohort_leaderboard`
**Description:** Infra layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `orm.cohort_leaderboard`, `repository.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_repo_impl.py` — `SQLAlchemyCohortLeaderboardRepository`

---

### Package: `service.cohort_leaderboard`
**Layer:** service
**Path:** `src/service/cohort_leaderboard`
**Description:** Service layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `domain.instructor`, `domain.student`, `domain.study_tip`, `dto.cohort_leaderboard`, `repository.cohort_leaderboard`, `service.cohort`, `service.nugget_wallet`, `service.student`
**Files:**
  - `cohort_leaderboard_service.py` — `REQ_COHORT_LEADERBOARD_01`

---

### Package: `api.cohort_leaderboard`
**Layer:** api
**Path:** `src/api/cohort_leaderboard`
**Description:** Api layer for the CohortLeaderboard domain class
**Tasks:** #115
**Depends on:** `dto.cohort_leaderboard`, `service.cohort_leaderboard`
**Files:**
  - `cohort_leaderboard_router.py` — `CohortLeaderboardRouter`

---

### Package: `tests.unit.cohort_leaderboard`
**Layer:** tests
**Path:** `tests/unit/cohort_leaderboard`
**Description:** Unit tests for CohortLeaderboard across domain, service, and API layers
**Tasks:** #115
**Depends on:** `domain.cohort_leaderboard`, `service.cohort_leaderboard`, `api.cohort_leaderboard`
**Files:**
  - `test_cohort_leaderboard_domain.py`
  - `test_cohort_leaderboard_service.py`
  - `test_cohort_leaderboard_api.py`

---

### Package: `domain.competency_trend_chart`
**Layer:** domain
**Path:** `src/domain/competency_trend_chart`
**Description:** Domain layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency`, `domain.question`, `domain.student`
**Files:**
  - `CompetencyTrendChart.py` — `Attempt`, `ChartPoint`, `CompetencyTrendChart`, `CompetencyTrendChartId`, `CompetencyTrendChartCreatedEvent`, `CompetencyTrendChartUpdatedEvent`

---

### Package: `dto.competency_trend_chart`
**Layer:** dto
**Path:** `src/dto/competency_trend_chart`
**Description:** Dto layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`
**Files:**
  - `competency_trend_chart_dto.py` — `CompetencyTrendChartCreateRequest`, `CompetencyTrendChartUpdateRequest`, `CompetencyTrendChartResponse`

---

### Package: `repository.competency_trend_chart`
**Layer:** repository
**Path:** `src/repository/competency_trend_chart`
**Description:** Repository layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency`, `domain.competency_trend_chart`, `service.competency_trend_chart`
**Files:**
  - `competency_trend_chart_repository.py` — `StudentDashboardUI`, `StudentDataAPI`, `TrendAPI`, `StudentDataStore`

---

### Package: `orm.competency_trend_chart`
**Layer:** orm
**Path:** `src/orm/competency_trend_chart`
**Description:** Orm layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`
**Files:**
  - `competency_trend_chart_orm.py` — `CompetencyTrendChartORM`

---

### Package: `infra.competency_trend_chart`
**Layer:** infra
**Path:** `src/infra/competency_trend_chart`
**Description:** Infra layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`, `orm.competency_trend_chart`, `repository.competency_trend_chart`
**Files:**
  - `competency_trend_chart_repo_impl.py` — `SQLAlchemyCompetencyTrendChartRepository`

---

### Package: `service.competency_trend_chart`
**Layer:** service
**Path:** `src/service/competency_trend_chart`
**Description:** Service layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `domain.competency`, `domain.competency_trend_chart`, `domain.student`, `domain.study_tip`, `dto.competency_trend_chart`, `repository.competency_trend_chart`, `service.competency`, `service.question`, `service.student`
**Files:**
  - `competency_trend_chart_service.py` — `PastAttemptData`, `DashboardData`, `TrendData`, `ReviewService`, `AccessControlService`, `Permission`, `Role`

---

### Package: `api.competency_trend_chart`
**Layer:** api
**Path:** `src/api/competency_trend_chart`
**Description:** Api layer for the CompetencyTrendChart domain class
**Tasks:** #116
**Depends on:** `dto.competency_trend_chart`, `service.competency_trend_chart`
**Files:**
  - `competency_trend_chart_router.py` — `ReviewController`

---

### Package: `tests.unit.competency_trend_chart`
**Layer:** tests
**Path:** `tests/unit/competency_trend_chart`
**Description:** Unit tests for CompetencyTrendChart across domain, service, and API layers
**Tasks:** #116
**Depends on:** `domain.competency_trend_chart`, `service.competency_trend_chart`, `api.competency_trend_chart`
**Files:**
  - `test_competency_trend_chart_domain.py`
  - `test_competency_trend_chart_service.py`
  - `test_competency_trend_chart_api.py`

---

### Package: `domain.enrollment`
**Layer:** domain
**Path:** `src/domain/enrollment`
**Description:** Domain layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.cohort`, `domain.student`, `domain.study_tip`
**Files:**
  - `Enrollment.py` — `Exam`, `Administrator`, `IT_Team`, `Enrollment`, `EnrollmentId`, `EnrollmentCreatedEvent`, `EnrollmentUpdatedEvent`

---

### Package: `dto.enrollment`
**Layer:** dto
**Path:** `src/dto/enrollment`
**Description:** Dto layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_dto.py` — `EnrollmentCreateRequest`, `EnrollmentUpdateRequest`, `EnrollmentResponse`

---

### Package: `repository.enrollment`
**Layer:** repository
**Path:** `src/repository/enrollment`
**Description:** Repository layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_repository.py` — `EnrollmentRepository`

---

### Package: `orm.enrollment`
**Layer:** orm
**Path:** `src/orm/enrollment`
**Description:** Orm layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`
**Files:**
  - `enrollment_orm.py` — `EnrollmentORM`

---

### Package: `infra.enrollment`
**Layer:** infra
**Path:** `src/infra/enrollment`
**Description:** Infra layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `orm.enrollment`, `repository.enrollment`
**Files:**
  - `enrollment_repo_impl.py` — `SQLAlchemyEnrollmentRepository`

---

### Package: `service.enrollment`
**Layer:** service
**Path:** `src/service/enrollment`
**Description:** Service layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `dto.enrollment`, `repository.enrollment`, `service.student`
**Files:**
  - `enrollment_service.py` — `EnrollmentService`, `EnrollmentServiceImpl`

---

### Package: `api.enrollment`
**Layer:** api
**Path:** `src/api/enrollment`
**Description:** Api layer for the Enrollment domain class
**Tasks:** #105, #108
**Depends on:** `dto.enrollment`, `service.enrollment`
**Files:**
  - `enrollment_router.py` — `EnrollmentRouter`

---

### Package: `tests.unit.enrollment`
**Layer:** tests
**Path:** `tests/unit/enrollment`
**Description:** Unit tests for Enrollment across domain, service, and API layers
**Tasks:** #105, #108
**Depends on:** `domain.enrollment`, `service.enrollment`, `api.enrollment`
**Files:**
  - `test_enrollment_domain.py`
  - `test_enrollment_service.py`
  - `test_enrollment_api.py`

---

### Package: `domain.exam_session`
**Layer:** domain
**Path:** `src/domain/exam_session`
**Description:** Domain layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.nugget_wallet`, `domain.question`, `domain.student`
**Files:**
  - `ExamSession.py` — `IT_Team`, `Exam`, `ExamSession`, `ExamStatus`, `Permission`, `ExamSessionId`, `ExamSessionCreatedEvent`, `ExamSessionUpdatedEvent`

---

### Package: `dto.exam_session`
**Layer:** dto
**Path:** `src/dto/exam_session`
**Description:** Dto layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_dto.py` — `ExamSessionCreateRequest`, `ExamSessionUpdateRequest`, `ExamSessionResponse`

---

### Package: `repository.exam_session`
**Layer:** repository
**Path:** `src/repository/exam_session`
**Description:** Repository layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_repository.py` — `ExamSessionRepository`

---

### Package: `orm.exam_session`
**Layer:** orm
**Path:** `src/orm/exam_session`
**Description:** Orm layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`
**Files:**
  - `exam_session_orm.py` — `ExamSessionORM`

---

### Package: `infra.exam_session`
**Layer:** infra
**Path:** `src/infra/exam_session`
**Description:** Infra layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`, `orm.exam_session`, `repository.exam_session`
**Files:**
  - `exam_session_repo_impl.py` — `SQLAlchemyExamSessionRepository`

---

### Package: `service.exam_session`
**Layer:** service
**Path:** `src/service/exam_session`
**Description:** Service layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `domain.exam_session`, `dto.exam_session`, `repository.exam_session`, `service.nugget_wallet`, `service.question`, `service.student`
**Files:**
  - `exam_session_service.py` — `ExamSessionService`, `ExamSessionServiceImpl`

---

### Package: `api.exam_session`
**Layer:** api
**Path:** `src/api/exam_session`
**Description:** Api layer for the ExamSession domain class
**Tasks:** #111
**Depends on:** `dto.exam_session`, `service.exam_session`
**Files:**
  - `exam_session_router.py` — `ExamSessionRouter`

---

### Package: `tests.unit.exam_session`
**Layer:** tests
**Path:** `tests/unit/exam_session`
**Description:** Unit tests for ExamSession across domain, service, and API layers
**Tasks:** #111
**Depends on:** `domain.exam_session`, `service.exam_session`, `api.exam_session`
**Files:**
  - `test_exam_session_domain.py`
  - `test_exam_session_service.py`
  - `test_exam_session_api.py`

---

### Package: `domain.instructor`
**Layer:** domain
**Path:** `src/domain/instructor`
**Description:** Domain layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.cohort`, `domain.competency`, `domain.enrollment`, `domain.exam_session`, `domain.question`, `domain.student`
**Files:**
  - `Instructor.py` — `Actor`, `Instructor`, `InstructorAccount`, `DashboardContent`, `Exam`, `Permission`, `InstructorId`, `InstructorCreatedEvent`, `InstructorUpdatedEvent`

---

### Package: `dto.instructor`
**Layer:** dto
**Path:** `src/dto/instructor`
**Description:** Dto layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_dto.py` — `InstructorCreateRequest`, `InstructorUpdateRequest`, `InstructorResponse`

---

### Package: `repository.instructor`
**Layer:** repository
**Path:** `src/repository/instructor`
**Description:** Repository layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_repository.py` — `Registration_API`, `Login_API`, `User_Database`, `Dashboard_UI`

---

### Package: `orm.instructor`
**Layer:** orm
**Path:** `src/orm/instructor`
**Description:** Orm layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`
**Files:**
  - `instructor_orm.py` — `InstructorORM`

---

### Package: `infra.instructor`
**Layer:** infra
**Path:** `src/infra/instructor`
**Description:** Infra layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`, `orm.instructor`, `repository.instructor`
**Files:**
  - `instructor_repo_impl.py` — `SQLAlchemyInstructorRepository`

---

### Package: `service.instructor`
**Layer:** service
**Path:** `src/service/instructor`
**Description:** Service layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `domain.instructor`, `dto.instructor`, `repository.instructor`, `service.competency`, `service.enrollment`
**Files:**
  - `instructor_service.py` — `InstructorService`, `InstructorServiceImpl`

---

### Package: `api.instructor`
**Layer:** api
**Path:** `src/api/instructor`
**Description:** Api layer for the Instructor domain class
**Tasks:** #105
**Depends on:** `dto.instructor`, `service.instructor`
**Files:**
  - `instructor_router.py` — `InstructorRouter`

---

### Package: `tests.unit.instructor`
**Layer:** tests
**Path:** `tests/unit/instructor`
**Description:** Unit tests for Instructor across domain, service, and API layers
**Tasks:** #105
**Depends on:** `domain.instructor`, `service.instructor`, `api.instructor`
**Files:**
  - `test_instructor_domain.py`
  - `test_instructor_service.py`
  - `test_instructor_api.py`

---

### Package: `domain.audit_event`
**Layer:** domain
**Path:** `src/domain/audit_event`
**Description:** Domain layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.instructor`, `domain.nugget_wallet`, `domain.student`
**Files:**
  - `AuditEvent.py` — `Permission`, `State`, `Teacher`, `IT_Team`, `BonusNugget`, `Justification`, `AuditEvent`, `AuditEventId`, `AuditEventCreatedEvent`, `AuditEventUpdatedEvent`

---

### Package: `dto.audit_event`
**Layer:** dto
**Path:** `src/dto/audit_event`
**Description:** Dto layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_dto.py` — `AuditEventCreateRequest`, `AuditEventUpdateRequest`, `AuditEventResponse`

---

### Package: `repository.audit_event`
**Layer:** repository
**Path:** `src/repository/audit_event`
**Description:** Repository layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_repository.py` — `AuditEventRepository`

---

### Package: `orm.audit_event`
**Layer:** orm
**Path:** `src/orm/audit_event`
**Description:** Orm layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`
**Files:**
  - `audit_event_orm.py` — `AuditEventORM`

---

### Package: `infra.audit_event`
**Layer:** infra
**Path:** `src/infra/audit_event`
**Description:** Infra layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`, `orm.audit_event`, `repository.audit_event`
**Files:**
  - `audit_event_repo_impl.py` — `SQLAlchemyAuditEventRepository`

---

### Package: `service.audit_event`
**Layer:** service
**Path:** `src/service/audit_event`
**Description:** Service layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`, `dto.audit_event`, `repository.audit_event`, `service.instructor`, `service.nugget_wallet`, `service.student`
**Files:**
  - `audit_event_service.py` — `AuditEventService`, `AuditEventServiceImpl`

---

### Package: `api.audit_event`
**Layer:** api
**Path:** `src/api/audit_event`
**Description:** Api layer for the AuditEvent domain class
**Tasks:** #109
**Depends on:** `dto.audit_event`, `service.audit_event`
**Files:**
  - `audit_event_router.py` — `AuditEventRouter`

---

### Package: `tests.unit.audit_event`
**Layer:** tests
**Path:** `tests/unit/audit_event`
**Description:** Unit tests for AuditEvent across domain, service, and API layers
**Tasks:** #109
**Depends on:** `domain.audit_event`, `service.audit_event`, `api.audit_event`
**Files:**
  - `test_audit_event_domain.py`
  - `test_audit_event_service.py`
  - `test_audit_event_api.py`

---

### Package: `domain.bonu_nugget_grant`
**Layer:** domain
**Path:** `src/domain/bonu_nugget_grant`
**Description:** Domain layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.audit_event`, `domain.instructor`, `domain.nugget_wallet`, `domain.student`
**Files:**
  - `BonuNuggetGrant.py` — `Permission`, `State`, `Teacher`, `IT_Team`, `BonusNugget`, `Justification`, `BonuNuggetGrant`, `BonuNuggetGrantId`, `BonuNuggetGrantCreatedEvent`, `BonuNuggetGrantUpdatedEvent`

---

### Package: `dto.bonu_nugget_grant`
**Layer:** dto
**Path:** `src/dto/bonu_nugget_grant`
**Description:** Dto layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_dto.py` — `BonuNuggetGrantCreateRequest`, `BonuNuggetGrantUpdateRequest`, `BonuNuggetGrantResponse`

---

### Package: `repository.bonu_nugget_grant`
**Layer:** repository
**Path:** `src/repository/bonu_nugget_grant`
**Description:** Repository layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_repository.py` — `BonuNuggetGrantRepository`

---

### Package: `orm.bonu_nugget_grant`
**Layer:** orm
**Path:** `src/orm/bonu_nugget_grant`
**Description:** Orm layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_orm.py` — `BonuNuggetGrantORM`

---

### Package: `infra.bonu_nugget_grant`
**Layer:** infra
**Path:** `src/infra/bonu_nugget_grant`
**Description:** Infra layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `orm.bonu_nugget_grant`, `repository.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_repo_impl.py` — `SQLAlchemyBonuNuggetGrantRepository`

---

### Package: `service.bonu_nugget_grant`
**Layer:** service
**Path:** `src/service/bonu_nugget_grant`
**Description:** Service layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `dto.bonu_nugget_grant`, `repository.bonu_nugget_grant`, `service.instructor`, `service.nugget_wallet`, `service.student`
**Files:**
  - `bonu_nugget_grant_service.py` — `BonuNuggetGrantService`, `BonuNuggetGrantServiceImpl`

---

### Package: `api.bonu_nugget_grant`
**Layer:** api
**Path:** `src/api/bonu_nugget_grant`
**Description:** Api layer for the BonuNuggetGrant domain class
**Tasks:** #109
**Depends on:** `dto.bonu_nugget_grant`, `service.bonu_nugget_grant`
**Files:**
  - `bonu_nugget_grant_router.py` — `BonuNuggetGrantRouter`

---

### Package: `tests.unit.bonu_nugget_grant`
**Layer:** tests
**Path:** `tests/unit/bonu_nugget_grant`
**Description:** Unit tests for BonuNuggetGrant across domain, service, and API layers
**Tasks:** #109
**Depends on:** `domain.bonu_nugget_grant`, `service.bonu_nugget_grant`, `api.bonu_nugget_grant`
**Files:**
  - `test_bonu_nugget_grant_domain.py`
  - `test_bonu_nugget_grant_service.py`
  - `test_bonu_nugget_grant_api.py`

---

### Package: `domain.instructor_dashboard`
**Layer:** domain
**Path:** `src/domain/instructor_dashboard`
**Description:** Domain layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.cohort`, `domain.competency`, `domain.enrollment`, `domain.exam_session`, `domain.instructor`, `domain.question`, `domain.student`
**Files:**
  - `InstructorDashboard.py` — `Actor`, `InstructorAccount`, `DashboardContent`, `Exam`, `Permission`, `InstructorDashboard`, `InstructorDashboardId`, `InstructorDashboardCreatedEvent`, `InstructorDashboardUpdatedEvent`

---

### Package: `dto.instructor_dashboard`
**Layer:** dto
**Path:** `src/dto/instructor_dashboard`
**Description:** Dto layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_dto.py` — `InstructorDashboardCreateRequest`, `InstructorDashboardUpdateRequest`, `InstructorDashboardResponse`

---

### Package: `repository.instructor_dashboard`
**Layer:** repository
**Path:** `src/repository/instructor_dashboard`
**Description:** Repository layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_repository.py` — `Registration_API`, `Login_API`, `User_Database`, `Dashboard_UI`

---

### Package: `orm.instructor_dashboard`
**Layer:** orm
**Path:** `src/orm/instructor_dashboard`
**Description:** Orm layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`
**Files:**
  - `instructor_dashboard_orm.py` — `InstructorDashboardORM`

---

### Package: `infra.instructor_dashboard`
**Layer:** infra
**Path:** `src/infra/instructor_dashboard`
**Description:** Infra layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `orm.instructor_dashboard`, `repository.instructor_dashboard`
**Files:**
  - `instructor_dashboard_repo_impl.py` — `SQLAlchemyInstructorDashboardRepository`

---

### Package: `service.instructor_dashboard`
**Layer:** service
**Path:** `src/service/instructor_dashboard`
**Description:** Service layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `dto.instructor_dashboard`, `repository.instructor_dashboard`, `service.competency`, `service.enrollment`
**Files:**
  - `instructor_dashboard_service.py` — `InstructorDashboardService`, `InstructorDashboardServiceImpl`

---

### Package: `api.instructor_dashboard`
**Layer:** api
**Path:** `src/api/instructor_dashboard`
**Description:** Api layer for the InstructorDashboard domain class
**Tasks:** #105
**Depends on:** `dto.instructor_dashboard`, `service.instructor_dashboard`
**Files:**
  - `instructor_dashboard_router.py` — `InstructorDashboardRouter`

---

### Package: `tests.unit.instructor_dashboard`
**Layer:** tests
**Path:** `tests/unit/instructor_dashboard`
**Description:** Unit tests for InstructorDashboard across domain, service, and API layers
**Tasks:** #105
**Depends on:** `domain.instructor_dashboard`, `service.instructor_dashboard`, `api.instructor_dashboard`
**Files:**
  - `test_instructor_dashboard_domain.py`
  - `test_instructor_dashboard_service.py`
  - `test_instructor_dashboard_api.py`

---

### Package: `domain.redemption`
**Layer:** domain
**Path:** `src/domain/redemption`
**Description:** Domain layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.instructor`, `domain.nugget_wallet`, `domain.student`, `domain.study_tip`
**Files:**
  - `Redemption.py` — `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `Redemption`, `RedemptionId`, `RedemptionCreatedEvent`, `RedemptionUpdatedEvent`

---

### Package: `dto.redemption`
**Layer:** dto
**Path:** `src/dto/redemption`
**Description:** Dto layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_dto.py` — `RedemptionCreateRequest`, `RedemptionUpdateRequest`, `RedemptionResponse`

---

### Package: `repository.redemption`
**Layer:** repository
**Path:** `src/repository/redemption`
**Description:** Repository layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_repository.py` — `RedemptionRepository`

---

### Package: `orm.redemption`
**Layer:** orm
**Path:** `src/orm/redemption`
**Description:** Orm layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`
**Files:**
  - `redemption_orm.py` — `RedemptionORM`

---

### Package: `infra.redemption`
**Layer:** infra
**Path:** `src/infra/redemption`
**Description:** Infra layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`, `orm.redemption`, `repository.redemption`
**Files:**
  - `redemption_repo_impl.py` — `SQLAlchemyRedemptionRepository`

---

### Package: `service.redemption`
**Layer:** service
**Path:** `src/service/redemption`
**Description:** Service layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `domain.redemption`, `domain.reward_store`, `domain.student`, `domain.study_tip`, `dto.redemption`, `repository.redemption`, `repository.study_tip`, `service.nugget_wallet`, `service.student`
**Files:**
  - `redemption_service.py` — `REQ_STU_01`

---

### Package: `api.redemption`
**Layer:** api
**Path:** `src/api/redemption`
**Description:** Api layer for the Redemption domain class
**Tasks:** #114
**Depends on:** `dto.redemption`, `service.redemption`
**Files:**
  - `redemption_router.py` — `RedemptionRouter`

---

### Package: `tests.unit.redemption`
**Layer:** tests
**Path:** `tests/unit/redemption`
**Description:** Unit tests for Redemption across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.redemption`, `service.redemption`, `api.redemption`
**Files:**
  - `test_redemption_domain.py`
  - `test_redemption_service.py`
  - `test_redemption_api.py`

---

### Package: `domain.reward_item`
**Layer:** domain
**Path:** `src/domain/reward_item`
**Description:** Domain layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.instructor`, `domain.nugget_wallet`, `domain.student`, `domain.study_tip`
**Files:**
  - `RewardItem.py` — `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `RewardItem`, `RewardItemId`, `RewardItemCreatedEvent`, `RewardItemUpdatedEvent`

---

### Package: `dto.reward_item`
**Layer:** dto
**Path:** `src/dto/reward_item`
**Description:** Dto layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_dto.py` — `RewardItemCreateRequest`, `RewardItemUpdateRequest`, `RewardItemResponse`

---

### Package: `repository.reward_item`
**Layer:** repository
**Path:** `src/repository/reward_item`
**Description:** Repository layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_repository.py` — `RewardItemRepository`

---

### Package: `orm.reward_item`
**Layer:** orm
**Path:** `src/orm/reward_item`
**Description:** Orm layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`
**Files:**
  - `reward_item_orm.py` — `RewardItemORM`

---

### Package: `infra.reward_item`
**Layer:** infra
**Path:** `src/infra/reward_item`
**Description:** Infra layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`, `orm.reward_item`, `repository.reward_item`
**Files:**
  - `reward_item_repo_impl.py` — `SQLAlchemyRewardItemRepository`

---

### Package: `service.reward_item`
**Layer:** service
**Path:** `src/service/reward_item`
**Description:** Service layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `domain.reward_item`, `domain.reward_store`, `domain.student`, `domain.study_tip`, `dto.reward_item`, `repository.reward_item`, `repository.study_tip`, `service.nugget_wallet`, `service.student`
**Files:**
  - `reward_item_service.py` — `REQ_STU_01`

---

### Package: `api.reward_item`
**Layer:** api
**Path:** `src/api/reward_item`
**Description:** Api layer for the RewardItem domain class
**Tasks:** #114
**Depends on:** `dto.reward_item`, `service.reward_item`
**Files:**
  - `reward_item_router.py` — `RewardItemRouter`

---

### Package: `tests.unit.reward_item`
**Layer:** tests
**Path:** `tests/unit/reward_item`
**Description:** Unit tests for RewardItem across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.reward_item`, `service.reward_item`, `api.reward_item`
**Files:**
  - `test_reward_item_domain.py`
  - `test_reward_item_service.py`
  - `test_reward_item_api.py`

---

### Package: `domain.reward_store`
**Layer:** domain
**Path:** `src/domain/reward_store`
**Description:** Domain layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.instructor`, `domain.nugget_wallet`, `domain.student`, `domain.study_tip`
**Files:**
  - `RewardStore.py` — `Actor`, `Resource`, `IfaceKind`, `Interface`, `RedemptionItem`, `NuggetBalance`, `ItemCost`, `RewardStore`, `RewardStoreId`, `RewardStoreCreatedEvent`, `RewardStoreUpdatedEvent`

---

### Package: `dto.reward_store`
**Layer:** dto
**Path:** `src/dto/reward_store`
**Description:** Dto layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_dto.py` — `RewardStoreCreateRequest`, `RewardStoreUpdateRequest`, `RewardStoreResponse`

---

### Package: `repository.reward_store`
**Layer:** repository
**Path:** `src/repository/reward_store`
**Description:** Repository layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_repository.py` — `RewardStoreRepository`

---

### Package: `orm.reward_store`
**Layer:** orm
**Path:** `src/orm/reward_store`
**Description:** Orm layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`
**Files:**
  - `reward_store_orm.py` — `RewardStoreORM`

---

### Package: `infra.reward_store`
**Layer:** infra
**Path:** `src/infra/reward_store`
**Description:** Infra layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`, `orm.reward_store`, `repository.reward_store`
**Files:**
  - `reward_store_repo_impl.py` — `SQLAlchemyRewardStoreRepository`

---

### Package: `service.reward_store`
**Layer:** service
**Path:** `src/service/reward_store`
**Description:** Service layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `domain.reward_store`, `domain.student`, `domain.study_tip`, `dto.reward_store`, `repository.reward_store`, `repository.study_tip`, `service.nugget_wallet`, `service.student`
**Files:**
  - `reward_store_service.py` — `REQ_STU_01`

---

### Package: `api.reward_store`
**Layer:** api
**Path:** `src/api/reward_store`
**Description:** Api layer for the RewardStore domain class
**Tasks:** #114
**Depends on:** `dto.reward_store`, `service.reward_store`
**Files:**
  - `reward_store_router.py` — `RewardStoreRouter`

---

### Package: `tests.unit.reward_store`
**Layer:** tests
**Path:** `tests/unit/reward_store`
**Description:** Unit tests for RewardStore across domain, service, and API layers
**Tasks:** #114
**Depends on:** `domain.reward_store`, `service.reward_store`, `api.reward_store`
**Files:**
  - `test_reward_store_domain.py`
  - `test_reward_store_service.py`
  - `test_reward_store_api.py`

---

### Package: `domain.streak`
**Layer:** domain
**Path:** `src/domain/streak`
**Description:** Domain layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.nugget_wallet`, `domain.question`, `domain.student`
**Files:**
  - `Streak.py` — `Player`, `Streak`, `StreakId`, `StreakCreatedEvent`, `StreakUpdatedEvent`

---

### Package: `dto.streak`
**Layer:** dto
**Path:** `src/dto/streak`
**Description:** Dto layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_dto.py` — `StreakCreateRequest`, `StreakUpdateRequest`, `StreakResponse`

---

### Package: `repository.streak`
**Layer:** repository
**Path:** `src/repository/streak`
**Description:** Repository layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_repository.py` — `Actor`, `Resource`, `Interface`, `Permission`, `State`, `IfaceKind`

---

### Package: `orm.streak`
**Layer:** orm
**Path:** `src/orm/streak`
**Description:** Orm layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`
**Files:**
  - `streak_orm.py` — `StreakORM`

---

### Package: `infra.streak`
**Layer:** infra
**Path:** `src/infra/streak`
**Description:** Infra layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`, `orm.streak`, `repository.streak`
**Files:**
  - `streak_repo_impl.py` — `SQLAlchemyStreakRepository`

---

### Package: `service.streak`
**Layer:** service
**Path:** `src/service/streak`
**Description:** Service layer for the Streak domain class
**Tasks:** #112
**Depends on:** `domain.streak`, `domain.study_tip`, `dto.streak`, `repository.streak`, `repository.study_tip`, `service.nugget_wallet`, `service.student`
**Files:**
  - `streak_service.py` — `Operation`

---

### Package: `api.streak`
**Layer:** api
**Path:** `src/api/streak`
**Description:** Api layer for the Streak domain class
**Tasks:** #112
**Depends on:** `dto.streak`, `service.streak`
**Files:**
  - `streak_router.py` — `StreakRouter`

---

### Package: `tests.unit.streak`
**Layer:** tests
**Path:** `tests/unit/streak`
**Description:** Unit tests for Streak across domain, service, and API layers
**Tasks:** #112
**Depends on:** `domain.streak`, `service.streak`, `api.streak`
**Files:**
  - `test_streak_domain.py`
  - `test_streak_service.py`
  - `test_streak_api.py`

---

### Package: `domain.student_profile`
**Layer:** domain
**Path:** `src/domain/student_profile`
**Description:** Domain layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.badge`, `domain.radar_chart`
**Files:**
  - `StudentProfile.py` — `StudentAccount`, `StudentProfile`, `RegistrationData`, `Avatar`, `StudentProfileId`, `StudentProfileCreatedEvent`, `StudentProfileUpdatedEvent`

---

### Package: `dto.student_profile`
**Layer:** dto
**Path:** `src/dto/student_profile`
**Description:** Dto layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_dto.py` — `StudentProfileCreateRequest`, `StudentProfileUpdateRequest`, `StudentProfileResponse`

---

### Package: `repository.student_profile`
**Layer:** repository
**Path:** `src/repository/student_profile`
**Description:** Repository layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_repository.py` — `StudentProfileRepository`

---

### Package: `orm.student_profile`
**Layer:** orm
**Path:** `src/orm/student_profile`
**Description:** Orm layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`
**Files:**
  - `student_profile_orm.py` — `StudentProfileORM`

---

### Package: `infra.student_profile`
**Layer:** infra
**Path:** `src/infra/student_profile`
**Description:** Infra layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`, `orm.student_profile`, `repository.student_profile`
**Files:**
  - `student_profile_repo_impl.py` — `SQLAlchemyStudentProfileRepository`

---

### Package: `service.student_profile`
**Layer:** service
**Path:** `src/service/student_profile`
**Description:** Service layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `domain.student_profile`, `dto.student_profile`, `repository.student_profile`
**Files:**
  - `student_profile_service.py` — `RegistrationService`, `RegistrationInput`

---

### Package: `api.student_profile`
**Layer:** api
**Path:** `src/api/student_profile`
**Description:** Api layer for the StudentProfile domain class
**Tasks:** #110
**Depends on:** `dto.student_profile`, `service.student_profile`
**Files:**
  - `student_profile_router.py` — `RegistrationController`

---

### Package: `tests.unit.student_profile`
**Layer:** tests
**Path:** `tests/unit/student_profile`
**Description:** Unit tests for StudentProfile across domain, service, and API layers
**Tasks:** #110
**Depends on:** `domain.student_profile`, `service.student_profile`, `api.student_profile`
**Files:**
  - `test_student_profile_domain.py`
  - `test_student_profile_service.py`
  - `test_student_profile_api.py`

---

### Package: `domain.study_tip`
**Layer:** domain
**Path:** `src/domain/study_tip`
**Description:** Domain layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.competency`, `domain.instructor`
**Files:**
  - `StudyTip.py` — `Actor`, `Students`, `Academic_Advisors`, `Instructors`, `Resource`, `StudentDashboardResource`, `ExamAnalysisAPIResource`, `Permission`, `State`, `StudyTip`, `StudyTipId`, `StudyTipCreatedEvent`, `StudyTipUpdatedEvent`

---

### Package: `dto.study_tip`
**Layer:** dto
**Path:** `src/dto/study_tip`
**Description:** Dto layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`
**Files:**
  - `study_tip_dto.py` — `StudyTipCreateRequest`, `StudyTipUpdateRequest`, `StudyTipResponse`

---

### Package: `repository.study_tip`
**Layer:** repository
**Path:** `src/repository/study_tip`
**Description:** Repository layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`, `repository.streak`
**Files:**
  - `study_tip_repository.py` — `Interface`, `Exam_Analysis_API`, `Student_Dashboard`

---

### Package: `orm.study_tip`
**Layer:** orm
**Path:** `src/orm/study_tip`
**Description:** Orm layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`
**Files:**
  - `study_tip_orm.py` — `StudyTipORM`

---

### Package: `infra.study_tip`
**Layer:** infra
**Path:** `src/infra/study_tip`
**Description:** Infra layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`, `orm.study_tip`, `repository.study_tip`
**Files:**
  - `study_tip_repo_impl.py` — `SQLAlchemyStudyTipRepository`

---

### Package: `service.study_tip`
**Layer:** service
**Path:** `src/service/study_tip`
**Description:** Service layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `domain.study_tip`, `dto.study_tip`, `repository.study_tip`, `service.competency`
**Files:**
  - `study_tip_service.py` — `REQ_EDU_01`

---

### Package: `api.study_tip`
**Layer:** api
**Path:** `src/api/study_tip`
**Description:** Api layer for the StudyTip domain class
**Tasks:** #113
**Depends on:** `dto.study_tip`, `service.study_tip`
**Files:**
  - `study_tip_router.py` — `StudyTipRouter`

---

### Package: `tests.unit.study_tip`
**Layer:** tests
**Path:** `tests/unit/study_tip`
**Description:** Unit tests for StudyTip across domain, service, and API layers
**Tasks:** #113
**Depends on:** `domain.study_tip`, `service.study_tip`, `api.study_tip`
**Files:**
  - `test_study_tip_domain.py`
  - `test_study_tip_service.py`
  - `test_study_tip_api.py`

---

### Package: `config.settings`
**Layer:** config
**Path:** `src/config`
**Description:** Application settings, environment variables, dependency injection
**Tasks:** None
**Depends on:** None
**Files:**
  - `settings.py` — `Settings`
  - `dependencies.py` — `Container`
  - `database.py`
  - `logging.py`

---

### Package: `docs.api_and_deployment`
**Layer:** docs
**Path:** `docs`
**Description:** OpenAPI documentation, admin guide, multi-city config, deployment runbook
**Tasks:** None
**Depends on:** None
**Files:**

---

### Package: `tests.integration`
**Layer:** tests
**Path:** `tests/integration`
**Description:** End-to-end and cross-service integration tests
**Tasks:** None
**Depends on:** `api.exam_builder`, `api.question`, `api.competency`, `api.schedule`, `api.student`, `api.student_profile`, `api.nugget_wallet`, `api.badge`, `api.radar_chart`, `api.competency_breakdown`, `api.study_tip`, `api.cohort`, `api.enrollment`, `api.attempt_review`, `api.competency_trend_chart`, `api.exam_session`, `api.streak`, `api.reward_store`, `api.reward_item`, `api.redemption`, `api.cohort_leaderboard`, `api.instructor`, `api.instructor_dashboard`, `api.bonu_nugget_grant`, `api.audit_event`
**Files:**
  - `test_exam_builder_flow.py`
  - `test_question_flow.py`
  - `test_competency_flow.py`
  - `test_schedule_flow.py`
  - `test_student_flow.py`
  - `test_student_profile_flow.py`
  - `test_nugget_wallet_flow.py`
  - `test_badge_flow.py`
  - `test_radar_chart_flow.py`
  - `test_competency_breakdown_flow.py`
  - `test_study_tip_flow.py`
  - `test_cohort_flow.py`
  - `test_enrollment_flow.py`
  - `test_attempt_review_flow.py`
  - `test_competency_trend_chart_flow.py`
  - `test_exam_session_flow.py`
  - `test_streak_flow.py`
  - `test_reward_store_flow.py`
  - `test_reward_item_flow.py`
  - `test_redemption_flow.py`
  - `test_cohort_leaderboard_flow.py`
  - `test_instructor_flow.py`
  - `test_instructor_dashboard_flow.py`
  - `test_bonu_nugget_grant_flow.py`
  - `test_audit_event_flow.py`
  - `test_api_contracts.py`
  - `conftest.py`

---

## Implementation

### Implementation #1 (Task #106)
**Task:** **As a** instructor
**Status:** ✅ All tests passing
**Timestamp:** 2026-06-29T21:39:34Z
**Test Result:** passed=10 failed=0
**Implemented Files:**
- `src/domain/exam_builder/ExamBuilder.py`
- `src/domain/question/Question.py`
- `src/domain/competency/Competency.py`
- `src/dto/question/question_dto.py`
- `src/domain/exam_builder/__init__.py`
- `src/domain/question/__init__.py`
- `src/domain/competency/__init__.py`
**Generated Tests:**
- `tests/unit/exam_builder/test_exam_builder_domain.py`
- `tests/unit/exam_builder/test_exam_builder_service.py`
- `tests/unit/exam_builder/test_exam_builder_api.py`

---

### Implementation #2 (Task #107)
**Task:** **As a** instructor
**Status:** ✅ All tests passing
**Timestamp:** 2026-06-29T21:43:02Z
**Test Result:** passed=12 failed=0
**Implemented Files:**
- `src/domain/schedule/Schedule.py`
- `src/domain/schedule/__init__.py`
- `src/dto/schedule/schedule_dto.py`
- `src/repository/schedule/schedule_repository.py`
- `src/orm/schedule/schedule_orm.py`
- `src/infra/schedule/schedule_repo_impl.py`
- `src/service/schedule/schedule_service.py`
- `src/service/schedule/__init__.py`
- `src/api/schedule/schedule_router.py`
- `src/orm/__init__.py`
- `main.py`
**Generated Tests:**
- `tests/unit/schedule/test_schedule_domain.py`
- `tests/unit/schedule/test_schedule_service.py`
- `tests/unit/schedule/test_schedule_api.py`

---

## Agent Status

**Last Updated:** {timestamp}
**Operations:** 0
**Errors:** 0

---

> Auto-generated by AI Agent

## Frontend Implementation

**Status:** completed
**Technology:** React + TypeScript (Vite)
**Directory:** experiments/project_14/frontend/
**Summary:** Built complete frontend for Gamified Competency Assessment Platform. Implemented 11 pages covering all user stories: Instructor Login/Register/Dashboard, Exam Builder, Cohort Management, Student Register/Profile, Take Exam (one-question-at-a-time with timer), Reward Store, Leaderboard, and Past Reviews. Used Apple-inspired design system. Build succeeds, 1 test passes.
**Files Created:**
  - src/types/index.ts
  - src/api/services.ts
  - src/components/Layout.tsx
  - src/pages/InstructorLoginPage.tsx
  - src/pages/InstructorRegisterPage.tsx
  - src/pages/InstructorDashboardPage.tsx
  - src/pages/ExamBuilderPage.tsx
  - src/pages/CohortsPage.tsx
  - src/pages/StudentRegisterPage.tsx
  - src/pages/StudentProfilePage.tsx
  - src/pages/TakeExamPage.tsx
  - src/pages/RewardStorePage.tsx
  - src/pages/LeaderboardPage.tsx

---

## Deployment

**Status:** ready
**Summary:** Full application stack (backend + frontend) for Gamified Competency Assessment Platform is operational. Backend starts directly and via Docker with PostgreSQL database. Frontend Vite production build succeeds. Docker containers (db, backend, frontend with nginx) all build and start healthy. DevOps configuration (nginx proxy, Vite rewrite, docker-compose services, healthcheck, DB driver, port conflicts) all verified and fixed.
**Start:** `bash start.sh`

---
