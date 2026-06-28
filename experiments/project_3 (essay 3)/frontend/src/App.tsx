
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import FlightsPage from './pages/FlightsPage'
import SlotsPage from './pages/SlotsPage'
import RunwaysPage from './pages/RunwaysPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/flights" element={<FlightsPage />} />
        <Route path="/slots" element={<SlotsPage />} />
        <Route path="/runways" element={<RunwaysPage />} />
      </Routes>
    </BrowserRouter>
  )
}
