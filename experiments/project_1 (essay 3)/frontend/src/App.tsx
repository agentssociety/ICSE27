import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import RegisterPage from './pages/RegisterPage'
import AssignUrgencyPage from './pages/AssignUrgencyPage'
import DequeuePage from './pages/DequeuePage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/assign-urgency" element={<AssignUrgencyPage />} />
          <Route path="/dequeue" element={<DequeuePage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
