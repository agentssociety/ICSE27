import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard' },
  { path: '/flights', label: 'Flights' },
  { path: '/slots', label: 'Slots' },
  { path: '/runways', label: 'Runways' },
  { path: '/timetable', label: 'Timetable' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  return (
    <div>
      <nav>
        <span style={{ fontWeight: 600, fontSize: '1.05rem', marginRight: 'auto' }}>
          ✈️ ATC Manager
        </span>
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            style={{
              color: location.pathname === item.path ? 'var(--accent)' : 'var(--text-secondary)',
              fontWeight: location.pathname === item.path ? 600 : 400,
              fontSize: '0.9rem',
            }}
          >
            {item.label}
          </Link>
        ))}
      </nav>
      <main>{children}</main>
    </div>
  );
}
