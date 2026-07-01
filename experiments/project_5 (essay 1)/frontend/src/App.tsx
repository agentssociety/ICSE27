import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import Layout from './components/Layout'
import InstructorLoginPage from './pages/InstructorLoginPage'
import InstructorRegisterPage from './pages/InstructorRegisterPage'
import InstructorDashboardPage from './pages/InstructorDashboardPage'
import ExamBuilderPage from './pages/ExamBuilderPage'
import CohortsPage from './pages/CohortsPage'
import StudentLoginPage from './pages/StudentLoginPage'
import StudentRegisterPage from './pages/StudentRegisterPage'
import StudentProfilePage from './pages/StudentProfilePage'
import TakeExamPage from './pages/TakeExamPage'
import RewardStorePage from './pages/RewardStorePage'
import LeaderboardPage from './pages/LeaderboardPage'
import AttemptReviewPage from './pages/AttemptReviewPage'
import CompetencyHeatmapPage from './pages/CompetencyHeatmapPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/instructor/login" element={<InstructorLoginPage />} />
          <Route path="/instructor/register" element={<InstructorRegisterPage />} />
          <Route path="/instructor/dashboard" element={<InstructorDashboardPage />} />
          <Route path="/instructor/exam-builder" element={<ExamBuilderPage />} />
          <Route path="/instructor/cohorts" element={<CohortsPage />} />
          <Route path="/instructor/heatmap" element={<CompetencyHeatmapPage />} />
          <Route path="/student/login" element={<StudentLoginPage />} />
          <Route path="/student/register" element={<StudentRegisterPage />} />
          <Route path="/student/profile" element={<StudentProfilePage />} />
          <Route path="/student/exam" element={<TakeExamPage />} />
          <Route path="/student/rewards" element={<RewardStorePage />} />
          <Route path="/student/leaderboard" element={<LeaderboardPage />} />
          <Route path="/student/reviews" element={<AttemptReviewPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
