from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infra.actor.actor_repo_impl import SQLAlchemyActorRepository
from src.infra.attempt.attempt_repo_impl import SQLAlchemyAttemptRepository
from src.infra.attempt_review.attempt_review_repo_impl import SQLAlchemyAttemptReviewRepository
from src.infra.avatar.avatar_repo_impl import SQLAlchemyAvatarRepository
from src.infra.badge.badge_repo_impl import SQLAlchemyBadgeRepository
from src.infra.bonu_nugget_grant.bonu_nugget_grant_repo_impl import SQLAlchemyBonuNuggetGrantRepository
from src.infra.bonus_nugget.bonus_nugget_repo_impl import SQLAlchemyBonusNuggetRepository
from src.infra.chart_point.chart_point_repo_impl import SQLAlchemyChartPointRepository
from src.infra.cohort_leaderboard.cohort_leaderboard_repo_impl import SQLAlchemyCohortLeaderboardRepository
from src.infra.competency.competency_repo_impl import SQLAlchemyCompetencyRepository
from src.infra.competency_trend_chart.competency_trend_chart_repo_impl import SQLAlchemyCompetencyTrendChartRepository
from src.infra.difficulty_tag.difficulty_tag_repo_impl import SQLAlchemyDifficultyTagRepository
from src.infra.enrollment.enrollment_repo_impl import SQLAlchemyEnrollmentRepository
from src.infra.exam.exam_repo_impl import SQLAlchemyExamRepository
from src.infra.it_team.it_team_repo_impl import SQLAlchemyIT_TeamRepository
from src.infra.interface.interface_repo_impl import SQLAlchemyInterfaceRepository
from src.infra.justification.justification_repo_impl import SQLAlchemyJustificationRepository
from src.infra.question.question_repo_impl import SQLAlchemyQuestionRepository
from src.infra.radar_chart.radar_chart_repo_impl import SQLAlchemyRadarChartRepository
from src.infra.registration_data.registration_data_repo_impl import SQLAlchemyRegistrationDataRepository
from src.infra.resource.resource_repo_impl import SQLAlchemyResourceRepository
from src.infra.student.student_repo_impl import SQLAlchemyStudentRepository
from src.infra.student_account.student_account_repo_impl import SQLAlchemyStudentAccountRepository
from src.infra.teacher.teacher_repo_impl import SQLAlchemyTeacherRepository


def get_actor_repository(db: Session = Depends(get_db)) -> SQLAlchemyActorRepository:
    return SQLAlchemyActorRepository(db)

def get_attempt_repository(db: Session = Depends(get_db)) -> SQLAlchemyAttemptRepository:
    return SQLAlchemyAttemptRepository(db)

def get_attempt_review_repository(db: Session = Depends(get_db)) -> SQLAlchemyAttemptReviewRepository:
    return SQLAlchemyAttemptReviewRepository(db)

def get_avatar_repository(db: Session = Depends(get_db)) -> SQLAlchemyAvatarRepository:
    return SQLAlchemyAvatarRepository(db)

def get_badge_repository(db: Session = Depends(get_db)) -> SQLAlchemyBadgeRepository:
    return SQLAlchemyBadgeRepository(db)

def get_bonu_nugget_grant_repository(db: Session = Depends(get_db)) -> SQLAlchemyBonuNuggetGrantRepository:
    return SQLAlchemyBonuNuggetGrantRepository(db)

def get_bonus_nugget_repository(db: Session = Depends(get_db)) -> SQLAlchemyBonusNuggetRepository:
    return SQLAlchemyBonusNuggetRepository(db)

def get_chart_point_repository(db: Session = Depends(get_db)) -> SQLAlchemyChartPointRepository:
    return SQLAlchemyChartPointRepository(db)

def get_cohort_leaderboard_repository(db: Session = Depends(get_db)) -> SQLAlchemyCohortLeaderboardRepository:
    return SQLAlchemyCohortLeaderboardRepository(db)

def get_competency_repository(db: Session = Depends(get_db)) -> SQLAlchemyCompetencyRepository:
    return SQLAlchemyCompetencyRepository(db)

def get_competency_trend_chart_repository(db: Session = Depends(get_db)) -> SQLAlchemyCompetencyTrendChartRepository:
    return SQLAlchemyCompetencyTrendChartRepository(db)

def get_difficulty_tag_repository(db: Session = Depends(get_db)) -> SQLAlchemyDifficultyTagRepository:
    return SQLAlchemyDifficultyTagRepository(db)

def get_enrollment_repository(db: Session = Depends(get_db)) -> SQLAlchemyEnrollmentRepository:
    return SQLAlchemyEnrollmentRepository(db)

def get_exam_repository(db: Session = Depends(get_db)) -> SQLAlchemyExamRepository:
    return SQLAlchemyExamRepository(db)

def get_it_team_repository(db: Session = Depends(get_db)) -> SQLAlchemyIT_TeamRepository:
    return SQLAlchemyIT_TeamRepository(db)

def get_interface_repository(db: Session = Depends(get_db)) -> SQLAlchemyInterfaceRepository:
    return SQLAlchemyInterfaceRepository(db)

def get_justification_repository(db: Session = Depends(get_db)) -> SQLAlchemyJustificationRepository:
    return SQLAlchemyJustificationRepository(db)

def get_question_repository(db: Session = Depends(get_db)) -> SQLAlchemyQuestionRepository:
    return SQLAlchemyQuestionRepository(db)

def get_radar_chart_repository(db: Session = Depends(get_db)) -> SQLAlchemyRadarChartRepository:
    return SQLAlchemyRadarChartRepository(db)

def get_registration_data_repository(db: Session = Depends(get_db)) -> SQLAlchemyRegistrationDataRepository:
    return SQLAlchemyRegistrationDataRepository(db)

def get_resource_repository(db: Session = Depends(get_db)) -> SQLAlchemyResourceRepository:
    return SQLAlchemyResourceRepository(db)

def get_student_repository(db: Session = Depends(get_db)) -> SQLAlchemyStudentRepository:
    return SQLAlchemyStudentRepository(db)

def get_student_account_repository(db: Session = Depends(get_db)) -> SQLAlchemyStudentAccountRepository:
    return SQLAlchemyStudentAccountRepository(db)

def get_teacher_repository(db: Session = Depends(get_db)) -> SQLAlchemyTeacherRepository:
    return SQLAlchemyTeacherRepository(db)