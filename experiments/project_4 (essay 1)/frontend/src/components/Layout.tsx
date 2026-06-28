import { Outlet, Link, useLocation } from 'react-router-dom';

export default function Layout() {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  return (
    <div>
      <nav>
        <Link to="/" style={{ fontWeight: isActive('/') ? 600 : 400, color: 'var(--text)' }}>
          Home
        </Link>
        <Link to="/login" style={{ fontWeight: isActive('/login') ? 600 : 400, color: 'var(--text)' }}>
          Login
        </Link>
        <Link to="/dashboard" style={{ fontWeight: isActive('/dashboard') ? 600 : 400, color: 'var(--text)' }}>
          Dashboard
        </Link>
        <Link to="/admin/accounts" style={{ fontWeight: isActive('/admin/accounts') ? 600 : 400, color: 'var(--text)' }}>
          Admin: Accounts
        </Link>
        <Link to="/admin/flagged" style={{ fontWeight: isActive('/admin/flagged') ? 600 : 400, color: 'var(--text)' }}>
          Flagged
        </Link>
        <Link to="/admin/transactions" style={{ fontWeight: isActive('/admin/transactions') ? 600 : 400, color: 'var(--text)' }}>
          Transactions
        </Link>
        <Link to="/admin/audit" style={{ fontWeight: isActive('/admin/audit') ? 600 : 400, color: 'var(--text)' }}>
          Audit Log
        </Link>
      </nav>
      <main className="page">
        <Outlet />
      </main>
    </div>
  );
}
