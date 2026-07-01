// ============================================================
// Type definitions matching backend Pydantic DTOs (API contract)
// ============================================================

// ---- Auth / Registration ----
export interface RegistrationData {
  name: string;
  email: string;
  password: string;
}

export interface RegistrationDataResponse {
  id: number;
  name: string;
  email: string;
  password: string;
}

// ---- Students ----
export interface StudentResponse {
  id: number;
  name: string;
  email: string;
  avatar_url?: string | null;
}

export interface StudentCreate {
  name: string;
  email: string;
  avatar_url?: string | null;
}

// ---- Student Accounts ----
export interface StudentAccountResponse {
  id: number;
  registrationData_id?: number | null;
}

export interface StudentAccountCreate {
  registrationData_id: number;
}

// ---- Teachers / Instructors ----
export interface TeacherResponse {
  id: number;
  name: string;
}

export interface TeacherCreate {
  name: string;
}

// ---- Exams ----
export interface ExamResponse {
  id: number;
  title: string;
  description?: string | null;
  instructor_id?: number | null;
  cohort_ids: number[];
  is_active: boolean;
}

export interface ExamCreate {
  title: string;
  description?: string | null;
  instructor_id?: number | null;
  cohort_ids?: number[];
  is_active?: boolean;
}

// ---- Questions ----
export type QuestionType = 'multiple_choice' | 'drag_and_drop' | 'code_snippet';
export type DifficultyTier = 'beginner' | 'intermediate' | 'advanced';

export interface QuestionResponse {
  id: number;
  type: QuestionType;
  difficulty_tier: DifficultyTier;
  nugget_reward_multiplier?: number | null;
  body?: string | null;
  answer_options?: string[] | null;
  correct_answer?: string | null;
  exam_id?: number | null;
  competency_ids: number[];
}

export interface QuestionCreate {
  type: QuestionType;
  difficulty_tier?: DifficultyTier | null;
  nugget_reward_multiplier?: number | null;
  body?: string | null;
  answer_options?: string[] | null;
  correct_answer?: string | null;
  exam_id?: number | null;
  competency_ids?: number[] | null;
}

// ---- Competencies ----
export interface CompetencyResponse {
  id: number;
  name: string;
}

export interface CompetencyCreate {
  name: string;
}

// ---- Cohorts ----
export interface CohortResponse {
  id: number;
  name: string;
  instructor_id?: number | null;
}

export interface CohortCreate {
  name: string;
  instructor_id?: number | null;
}

// ---- Cohort Leaderboard ----
export interface CohortLeaderboardResponse {
  id: number;
  student_id?: number | null;
}

// ---- Enrollments ----
export interface EnrollmentResponse {
  id: number;
  student_id: number;
  cohort_id?: number | null;
  exam_id?: number | null;
}

export interface EnrollmentCreate {
  student_id: number;
  cohort_id?: number | null;
  exam_id?: number | null;
}

// ---- Schedules ----
export interface ScheduleResponse {
  id: number;
  exam_id: string;
  open_date: string;
  close_date: string;
  per_attempt_time_limit_minutes?: number | null;
}

export interface ScheduleCreateRequest {
  exam_id: string;
  open_date: string;
  close_date: string;
  per_attempt_time_limit_minutes?: number | null;
}

// ---- Attempts ----
export interface AttemptResponse {
  id: number;
  method_isCompleted: boolean;
  student_id?: number | null;
}

export interface AttemptCreate {
  method_isCompleted: boolean;
  student_id: number;
}

// ---- Attempt Reviews ----
export interface AttemptReviewResponse {
  id: number;
  competency_id?: number | null;
  question_id?: number | null;
  student_id?: number | null;
}

// ---- Bonus Nuggets ----
export interface BonusNuggetResponse {
  id: number;
  student_id: number;
  instructor_id?: number | null;
  amount: number;
  justification: string;
}

export interface BonusNuggetCreate {
  student_id: number;
  instructor_id?: number | null;
  amount: number;
  justification: string;
}

// ---- Reward Items ----
export interface RewardItemResponse {
  id: number;
  name: string;
  description?: string | null;
  cost: number;
  item_type: string;
  instructor_id?: number | null;
}

export interface RewardItemCreate {
  name: string;
  description?: string | null;
  cost: number;
  item_type?: string;
  instructor_id?: number | null;
}

// ---- Competency Breakdown ----
export interface CompetencyBreakdownResponse {
  id: number;
  exam_session_id: number;
  competency_name: string;
  score: number;
  max_score: number;
  is_weak: boolean;
}

// ---- Study Tips ----
export interface StudyTipResponse {
  id: number;
  competency_name?: string | null;
  title: string;
  content?: string | null;
}

// ---- Student Profile ----
export interface StudentProfileResponse {
  id: number;
  student_id: number;
  avatar_url?: string | null;
  bio?: string | null;
}

export interface StudentProfileCreate {
  student_id: number;
  avatar_url?: string | null;
  bio?: string | null;
}

// ---- Nugget Wallet ----
export interface NuggetWalletResponse {
  id: number;
  student_id: number;
  balance: number;
}

export interface NuggetWalletCreate {
  student_id: number;
  balance?: number;
}

// ---- Badges ----
export interface BadgeResponse {
  id: number;
  name: string;
  description: string;
  student_id?: number | null;
}

export interface BadgeCreate {
  name: string;
  description: string;
  student_id?: number | null;
}

// ---- Avatars ----
export interface AvatarResponse {
  id: number;
  imageUrl: string;
}

// ---- Radar Charts ----
export interface RadarChartResponse {
  id: number;
  competencies: Record<string, number>;
}

// ---- Justifications ----
export interface JustificationResponse {
  id: number;
  text: string;
  teacherId: string;
}

// ---- Resources ----
export interface ResourceResponse {
  id: number;
  owner_id?: number | null;
}

// ---- Difficulty Tags ----
export interface DifficultyTagResponse {
  id: number;
  resource_id?: number | null;
}

// ---- Streaks ----
export interface StreakResponse {
  id: number;
  student_id: number;
  current_streak: number;
  longest_streak: number;
  multiplier: number;
}

export interface StreakCreate {
  student_id: number;
}

// ---- Exam Sessions ----
export interface ExamSessionResponse {
  id: number;
  student_id?: number | null;
  exam_id?: number | null;
  answers: Record<string, string>;
}

// ---- Chart Points ----
export interface ChartPointResponse {
  id: number;
  value: number;
  label: string;
}

// ---- Competency Trend Charts ----
export interface CompetencyTrendChartResponse {
  id: number;
  competency_id?: number | null;
  question_id?: number | null;
  student_id?: number | null;
}

// ---- Redemption ----
export interface RedemptionResponse {
  id: number;
  student_id?: number | null;
  reward_item_id?: number | null;
  nuggets_spent?: number | null;
  redeemed_at?: string | null;
}

// ---- Instructor Dashboard ----
export interface InstructorDashboardResponse {
  id: number;
  instructor_id?: number | null;
  active_exams: ExamResponse[];
  enrollment_counts: Record<string, number>;
  competency_coverage: Record<string, number>;
}

