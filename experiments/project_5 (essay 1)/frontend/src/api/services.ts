// ============================================================
// API Service Layer - All calls use /api/... for Vite proxy
// ============================================================
import axios from 'axios';
import type {
  ExamResponse, ExamCreate,
  QuestionResponse, QuestionCreate,
  StudentResponse, StudentCreate,
  TeacherResponse, TeacherCreate,
  CompetencyResponse, CompetencyCreate,
  CohortResponse, CohortCreate,
  ScheduleResponse, ScheduleCreateRequest,
  AttemptResponse, AttemptCreate,
  AttemptReviewResponse,
  BonusNuggetResponse, BonusNuggetCreate,
  BadgeResponse, BadgeCreate,
  AvatarResponse,
  RadarChartResponse,
  JustificationResponse,
  CohortLeaderboardResponse,
  EnrollmentResponse, EnrollmentCreate,
  RegistrationData, RegistrationDataResponse,
  StudentAccountResponse, StudentAccountCreate,
  ExamSessionResponse,
  StudyTipResponse,
  NuggetWalletResponse, NuggetWalletCreate,
  StreakResponse, StreakCreate,
  ChartPointResponse,
  CompetencyTrendChartResponse,
  RedemptionResponse,
  RewardItemResponse, RewardItemCreate,
  CompetencyBreakdownResponse,
  StudentProfileResponse, StudentProfileCreate,
  InstructorDashboardResponse,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// ---- Health ----
export const checkHealth = () => api.get('/health');

// ---- Auth / Registration ----
export const createRegistration = (data: RegistrationData) =>
  api.post<RegistrationDataResponse>('/registration_datas', data);

export const getRegistrations = () =>
  api.get<RegistrationDataResponse[]>('/registration_datas');

// ---- Students ----
export const createStudent = (data: StudentCreate) =>
  api.post<StudentResponse>('/students', data);

export const getStudents = () =>
  api.get<StudentResponse[]>('/students');

export const getStudent = (id: string) =>
  api.get<StudentResponse>(`/students/${id}`);

export const updateStudent = (id: string, data: Partial<StudentCreate>) =>
  api.put<StudentResponse>(`/students/${id}`, data);

// ---- Student Accounts ----
export const createStudentAccount = (data: StudentAccountCreate) =>
  api.post<StudentAccountResponse>('/student_accounts', data);

// ---- Teachers ----
export const createTeacher = (data: TeacherCreate) =>
  api.post<TeacherResponse>('/teachers', data);

export const getTeachers = () =>
  api.get<TeacherResponse[]>('/teachers');

export const getTeacher = (id: string) =>
  api.get<TeacherResponse>(`/teachers/${id}`);

// ---- Exams ----
export const getExams = () =>
  api.get<ExamResponse[]>('/exams');

export const getExam = (id: string) =>
  api.get<ExamResponse>(`/exams/${id}`);

export const createExam = (data: ExamCreate) =>
  api.post<ExamResponse>('/exams', data);

export const updateExam = (id: string, data: Partial<ExamCreate>) =>
  api.put<ExamResponse>(`/exams/${id}`, data);

export const deleteExam = (id: string) =>
  api.delete(`/exams/${id}`);

// ---- Questions ----
export const getQuestions = (examId?: number) =>
  api.get<QuestionResponse[]>('/questions', { params: examId ? { exam_id: examId } : {} });

export const getQuestion = (id: number) =>
  api.get<QuestionResponse>(`/questions/${id}`);

export const createQuestion = (data: QuestionCreate) =>
  api.post<QuestionResponse>('/questions', data);

export const updateQuestion = (id: number, data: Partial<QuestionCreate>) =>
  api.put<QuestionResponse>(`/questions/${id}`, data);

export const deleteQuestion = (id: number) =>
  api.delete(`/questions/${id}`);

// ---- Competencies ----
export const getCompetencies = () =>
  api.get<CompetencyResponse[]>('/competencys');

export const createCompetency = (data: CompetencyCreate) =>
  api.post<CompetencyResponse>('/competencys', data);

// ---- Schedules ----
export const getSchedules = () =>
  api.get<ScheduleResponse[]>('/schedules');

export const createSchedule = (data: ScheduleCreateRequest) =>
  api.post<ScheduleResponse>('/schedules', data);

export const updateSchedule = (id: number, data: Partial<ScheduleCreateRequest>) =>
  api.put<ScheduleResponse>(`/schedules/${id}`, data);

// ---- Cohorts ----
export const getCohorts = () =>
  api.get<CohortResponse[]>('/cohorts');

export const createCohort = (data: CohortCreate) =>
  api.post<CohortResponse>('/cohorts', data);

// ---- Enrollments ----
export const getEnrollments = () =>
  api.get<EnrollmentResponse[]>('/enrollments');

export const createEnrollment = (data: EnrollmentCreate) =>
  api.post<EnrollmentResponse>('/enrollments', data);

// ---- Attempts ----
export const getAttempts = () =>
  api.get<AttemptResponse[]>('/attempts');

export const createAttempt = (data: AttemptCreate) =>
  api.post<AttemptResponse>('/attempts', data);

// ---- Attempt Reviews ----
export const getAttemptReviews = () =>
  api.get<AttemptReviewResponse[]>('/attempt_reviews');

// ---- Bonus Nuggets (bonu_nugget_grants) ----
export const getBonusNuggets = () =>
  api.get<BonusNuggetResponse[]>('/bonu_nugget_grants');

export const createBonusNugget = (data: BonusNuggetCreate) =>
  api.post<BonusNuggetResponse>('/bonu_nugget_grants', data);

// ---- Badges ----
export const getBadges = (studentId?: number) =>
  api.get<BadgeResponse[]>('/badges', { params: studentId ? { student_id: studentId } : {} });

export const createBadge = (data: BadgeCreate) =>
  api.post<BadgeResponse>('/badges', data);

// ---- Avatars ----
export const getAvatars = () =>
  api.get<AvatarResponse[]>('/avatars');

// ---- Radar Charts ----
export const getRadarCharts = () =>
  api.get<RadarChartResponse[]>('/radar_charts');

// ---- Cohort Leaderboards ----
export const getCohortLeaderboards = () =>
  api.get<CohortLeaderboardResponse[]>('/cohort_leaderboards');

// ---- Justifications ----
export const getJustifications = () =>
  api.get<JustificationResponse[]>('/justifications');

// ---- Exam Sessions ----
export const getExamSessions = () =>
  api.get<ExamSessionResponse[]>('/exam_sessions');

export const createExamSession = (data: { student_id: number; exam_id: number; answers: Record<string, string> }) =>
  api.post<ExamSessionResponse>('/exam_sessions', data);

// ---- Nugget Wallet ----
export const getNuggetWallets = (studentId?: number) =>
  api.get<NuggetWalletResponse[]>('/nugget_wallets', { params: studentId ? { student_id: studentId } : {} });

export const createNuggetWallet = (data: NuggetWalletCreate) =>
  api.post<NuggetWalletResponse>('/nugget_wallets', data);

export const updateNuggetWallet = (id: number, data: { balance: number }) =>
  api.put<NuggetWalletResponse>(`/nugget_wallets/${id}`, data);

// ---- Streaks ----
export const getStreaks = (studentId?: number) =>
  api.get<StreakResponse[]>('/streaks', { params: studentId ? { student_id: studentId } : {} });

export const createStreak = (data: StreakCreate) =>
  api.post<StreakResponse>('/streaks', data);

export const recordCorrectAnswer = (streakId: number) =>
  api.post<StreakResponse>(`/streaks/${streakId}/correct`);

export const recordWrongAnswer = (streakId: number) =>
  api.post<StreakResponse>(`/streaks/${streakId}/wrong`);

// ---- Reward Items ----
export const getRewardItems = () =>
  api.get<RewardItemResponse[]>('/reward_items');

export const createRewardItem = (data: RewardItemCreate) =>
  api.post<RewardItemResponse>('/reward_items', data);

// ---- Redemptions ----
export const createRedemption = (data: { student_id: number; reward_item_id: number; nuggets_spent: number }) =>
  api.post<RedemptionResponse>('/redemptions', data);

export const getRedemptions = (studentId?: number) =>
  api.get<RedemptionResponse[]>('/redemptions', { params: studentId ? { student_id: studentId } : {} });

// ---- Competency Breakdowns ----
export const getCompetencyBreakdowns = (examSessionId?: number) =>
  api.get<CompetencyBreakdownResponse[]>('/competency_breakdowns', { params: examSessionId ? { exam_session_id: examSessionId } : {} });

export const createCompetencyBreakdown = (data: any) =>
  api.post<CompetencyBreakdownResponse>('/competency_breakdowns', data);

// ---- Study Tips ----
export const getStudyTips = (competencyName?: string) =>
  api.get<StudyTipResponse[]>('/study_tips', { params: competencyName ? { competency_name: competencyName } : {} });

// ---- Student Profiles ----
export const getStudentProfiles = (studentId?: number) =>
  api.get<StudentProfileResponse[]>('/student_profiles', { params: studentId ? { student_id: studentId } : {} });

export const createStudentProfile = (data: StudentProfileCreate) =>
  api.post<StudentProfileResponse>('/student_profiles', data);

export const updateStudentProfile = (id: number, data: Partial<StudentProfileCreate>) =>
  api.put<StudentProfileResponse>(`/student_profiles/${id}`, data);

// ---- Chart Points ----
export const getChartPoints = () =>
  api.get<ChartPointResponse[]>('/chart_points');

// ---- Competency Trend Charts ----
export const getCompetencyTrendCharts = () =>
  api.get<CompetencyTrendChartResponse[]>('/competency_trend_charts');

// ---- Instructor Dashboard ----
export const getInstructorDashboard = () =>
  api.get<InstructorDashboardResponse>('/instructor_dashboards');

export default api;
