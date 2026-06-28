import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/login', label: 'Login' },
  { path: '/accounts', label: 'Accounts' },
  { path: '/withdrawals', label: 'Withdrawals' },
  { path: '/flagged', label: 'Flagged' },
  { path: '/users', label: 'Users' },
  { path: '/audit-logs', label: 'Audit Logs' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  return (
    <div>
      <nav>
        <Link to="/" style={{ fontWeight: 600, fontSize: '1.05rem', color: 'var(--text)' }}>
          ATM System
        </Link>
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={location.pathname === item.path ? 'active' : ''}
            style={{
              color: location.pathname === item.path ? 'var(--accent)' : 'var(--text-secondary)',
              fontWeight: location.pathname === item.path ? 500 : 400,
              fontSize: '0.9rem',
            }}
          >
            {item.label}
          </Link>
        ))}
      </nav>
      <main className="page">
        {children}
      </main>
    </div>
  );
}
