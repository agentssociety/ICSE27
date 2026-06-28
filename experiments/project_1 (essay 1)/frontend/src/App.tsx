import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import RegisterPatientPage from './pages/RegisterPatientPage'
import QueuePage from './pages/QueuePage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/register" element={<RegisterPatientPage />} />
          <Route path="/queue" element={<QueuePage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
