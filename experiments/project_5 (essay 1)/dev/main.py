from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config.database import create_tables
from src.config.settings import settings
from src.api.actor.actor_router import router as actor_router
from src.api.attempt.attempt_router import router as attempt_router
from src.api.attempt_review.attempt_review_router import router as attempt_review_router
from src.api.audit_event.audit_event_router import router as audit_event_router
from src.api.avatar.avatar_router import router as avatar_router
from src.api.badge.badge_router import router as badge_router
from src.api.bonu_nugget_grant.bonu_nugget_grant_router import router as bonu_nugget_grant_router
from src.api.bonus_nugget.bonus_nugget_router import router as bonus_nugget_router
from src.api.chart_point.chart_point_router import router as chart_point_router
from src.api.cohort.cohort_router import router as cohort_router
from src.api.cohort_leaderboard.cohort_leaderboard_router import router as cohort_leaderboard_router
from src.api.competency.competency_router import router as competency_router
from src.api.competency_breakdown.competency_breakdown_router import router as competency_breakdown_router
from src.api.competency_trend_chart.competency_trend_chart_router import router as competency_trend_chart_router
from src.api.difficulty_tag.difficulty_tag_router import router as difficulty_tag_router
from src.api.enrollment.enrollment_router import router as enrollment_router
from src.api.exam.exam_router import router as exam_router
from src.api.exam_session.exam_session_router import router as exam_session_router
from src.api.it_team.it_team_router import router as it_team_router
from src.api.interface.interface_router import router as interface_router
from src.api.justification.justification_router import router as justification_router
from src.api.nugget_wallet.nugget_wallet_router import router as nugget_wallet_router
from src.api.question.question_router import router as question_router
from src.api.radar_chart.radar_chart_router import router as radar_chart_router
from src.api.redemption.redemption_router import router as redemption_router
from src.api.registration_data.registration_data_router import router as registration_data_router
from src.api.resource.resource_router import router as resource_router
from src.api.reward_item.reward_item_router import router as reward_item_router
from src.api.reward_store.reward_store_router import router as reward_store_router
from src.api.schedule.schedule_router import router as schedule_router
from src.api.streak.streak_router import router as streak_router
from src.api.student.student_router import router as student_router
from src.api.student_account.student_account_router import router as student_account_router
from src.api.student_profile.student_profile_router import router as student_profile_router
from src.api.study_tip.study_tip_router import router as study_tip_router
from src.api.teacher.teacher_router import router as teacher_router

_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        _log.info("Database tables created / verified.")
    except Exception as exc:
        _log.warning("DB unavailable at startup (will retry per request): %s", exc)
    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Auto-generated API",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actor_router, prefix="/actors", tags=["Actor"])
app.include_router(attempt_router, prefix="/attempts", tags=["Attempt"])
app.include_router(attempt_review_router, prefix="/attempt_reviews", tags=["AttemptReview"])
app.include_router(audit_event_router, prefix="/audit_events", tags=["AuditEvent"])
app.include_router(avatar_router, prefix="/avatars", tags=["Avatar"])
app.include_router(badge_router, prefix="/badges", tags=["Badge"])
app.include_router(bonu_nugget_grant_router, prefix="/bonu_nugget_grants", tags=["BonuNuggetGrant"])
app.include_router(bonus_nugget_router, prefix="/bonus_nuggets", tags=["BonusNugget"])
app.include_router(chart_point_router, prefix="/chart_points", tags=["ChartPoint"])
app.include_router(cohort_router, prefix="/cohorts", tags=["Cohort"])
app.include_router(cohort_leaderboard_router, prefix="/cohort_leaderboards", tags=["CohortLeaderboard"])
app.include_router(competency_router, prefix="/competencys", tags=["Competency"])
app.include_router(competency_breakdown_router, prefix="/competency_breakdowns", tags=["CompetencyBreakdown"])
app.include_router(competency_trend_chart_router, prefix="/competency_trend_charts", tags=["CompetencyTrendChart"])
app.include_router(difficulty_tag_router, prefix="/difficulty_tags", tags=["DifficultyTag"])
app.include_router(enrollment_router, prefix="/enrollments", tags=["Enrollment"])
app.include_router(exam_router, prefix="/exams", tags=["Exam"])
app.include_router(exam_session_router, prefix="/exam_sessions", tags=["ExamSession"])
app.include_router(it_team_router, prefix="/it_teams", tags=["IT_Team"])
app.include_router(interface_router, prefix="/interfaces", tags=["Interface"])
app.include_router(justification_router, prefix="/justifications", tags=["Justification"])
app.include_router(nugget_wallet_router, prefix="/nugget_wallets", tags=["NuggetWallet"])
app.include_router(question_router, prefix="/questions", tags=["Question"])
app.include_router(radar_chart_router, prefix="/radar_charts", tags=["RadarChart"])
app.include_router(redemption_router, prefix="/redemptions", tags=["Redemption"])
app.include_router(registration_data_router, prefix="/registration_datas", tags=["RegistrationData"])
app.include_router(resource_router, prefix="/resources", tags=["Resource"])
app.include_router(reward_item_router, prefix="/reward_items", tags=["RewardItem"])
app.include_router(reward_store_router, prefix="/reward_stores", tags=["RewardStore"])
app.include_router(schedule_router, prefix="/schedules", tags=["Schedule"])
app.include_router(streak_router, prefix="/streaks", tags=["Streak"])
app.include_router(student_router, prefix="/students", tags=["Student"])
app.include_router(student_account_router, prefix="/student_accounts", tags=["StudentAccount"])
app.include_router(student_profile_router, prefix="/student_profiles", tags=["StudentProfile"])
app.include_router(study_tip_router, prefix="/study_tips", tags=["StudyTip"])
app.include_router(teacher_router, prefix="/teachers", tags=["Teacher"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")