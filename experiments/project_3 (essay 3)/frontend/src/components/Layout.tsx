
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/flights', label: 'Flights' },
  { path: '/slots', label: 'Slots' },
  { path: '/runways', label: 'Runways' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  return (
    <div>
      <nav>
        <Link to="/" style={{ fontWeight: 600, fontSize: '1.125rem', color: 'var(--text)', textDecoration: 'none' }}>
          Airport Scheduler
        </Link>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {navItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                padding: '0.375rem 0.75rem',
                borderRadius: 'var(--radius-s)',
                fontSize: '0.875rem',
                fontWeight: 500,
                color: location.pathname === item.path ? 'var(--accent)' : 'var(--text-secondary)',
                background: location.pathname === item.path ? 'var(--bg-secondary)' : 'transparent',
                textDecoration: 'none',
                transition: 'all var(--ease)',
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
}
