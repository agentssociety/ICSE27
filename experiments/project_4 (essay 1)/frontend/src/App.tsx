import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import AdminAccountsPage from './pages/AdminAccountsPage'
import AdminFlaggedTransactionsPage from './pages/AdminFlaggedTransactionsPage'
import AdminTransactionsPage from './pages/AdminTransactionsPage'
import AdminAuditLogPage from './pages/AdminAuditLogPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/admin/accounts" element={<AdminAccountsPage />} />
          <Route path="/admin/flagged" element={<AdminFlaggedTransactionsPage />} />
          <Route path="/admin/transactions" element={<AdminTransactionsPage />} />
          <Route path="/admin/audit" element={<AdminAuditLogPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
