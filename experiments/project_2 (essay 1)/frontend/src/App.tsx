import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import BloodUnitsPage from "./pages/BloodUnitsPage";
import TransfusionRequestsPage from "./pages/TransfusionRequestsPage";
import ReservationsPage from "./pages/ReservationsPage";
import DashboardPage from "./pages/DashboardPage";

function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout />
      <Routes>
        <Route path="/" element={<h1 style={{ textAlign: "center", marginTop: "3rem" }}>Blood Bank Inventory Manager</h1>} />
        <Route path="/blood-units" element={<BloodUnitsPage />} />
        <Route path="/transfusion-requests" element={<TransfusionRequestsPage />} />
        <Route path="/reservations" element={<ReservationsPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
