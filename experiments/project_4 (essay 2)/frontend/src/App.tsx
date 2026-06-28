import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import AuditLogPage from './pages/AuditLogPage'
import FlaggedTransactionsPage from './pages/FlaggedTransactionsPage'
import AdminAccountsPage from './pages/AdminAccountsPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/audit-log" element={<AuditLogPage />} />
          <Route path="/flagged-transactions" element={<FlaggedTransactionsPage />} />
          <Route path="/admin/accounts" element={<AdminAccountsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
