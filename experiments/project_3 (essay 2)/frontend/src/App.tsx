import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import FlightsPage from './pages/FlightsPage'
import SlotsPage from './pages/SlotsPage'
import RunwaysPage from './pages/RunwaysPage'
import TimetablePage from './pages/TimetablePage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/flights" element={<FlightsPage />} />
          <Route path="/slots" element={<SlotsPage />} />
          <Route path="/runways" element={<RunwaysPage />} />
          <Route path="/timetable" element={<TimetablePage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
