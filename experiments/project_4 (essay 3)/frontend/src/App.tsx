import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import LoginPage from './pages/LoginPage'
import AccountsPage from './pages/AccountsPage'
import WithdrawalsPage from './pages/WithdrawalsPage'
import FlaggedPage from './pages/FlaggedPage'
import UsersPage from './pages/UsersPage'
import AuditLogsPage from './pages/AuditLogsPage'

export default function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/accounts" element={<AccountsPage />} />
          <Route path="/withdrawals" element={<WithdrawalsPage />} />
          <Route path="/flagged" element={<FlaggedPage />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/audit-logs" element={<AuditLogsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
