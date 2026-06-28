import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import FlightsPage from './pages/FlightsPage'
import SlotsPage from './pages/SlotsPage'
import RunwaysPage from './pages/RunwaysPage'
import EmergencyFlightsPage from './pages/EmergencyFlightsPage'
import TimetablePage from './pages/TimetablePage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/flights" element={<FlightsPage />} />
          <Route path="/slots" element={<SlotsPage />} />
          <Route path="/runways" element={<RunwaysPage />} />
          <Route path="/emergency" element={<EmergencyFlightsPage />} />
          <Route path="/timetable" element={<TimetablePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
