import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import BloodUnitsPage from './pages/BloodUnitsPage'
import TransfusionRequestsPage from './pages/TransfusionRequestsPage'
import ReservationsPage from './pages/ReservationsPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/blood-units" element={<BloodUnitsPage />} />
          <Route path="/transfusion-requests" element={<TransfusionRequestsPage />} />
          <Route path="/reservations" element={<ReservationsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
