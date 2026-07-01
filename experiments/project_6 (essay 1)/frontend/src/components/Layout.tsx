
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const NAV_ITEMS = [
  { path: '/', label: 'Feed' },
  { path: '/profile', label: 'Profile' },
  { path: '/groups', label: 'Groups' },
  { path: '/notifications', label: 'Notifications' },
  { path: '/messages', label: 'Messages' },
  { path: '/search', label: 'Search' },
  { path: '/settings', label: 'Settings' },
  { path: '/admin', label: 'Admin' },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/register');
  };

  return (
    <>
      {user && (
        <nav>
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                fontWeight: location.pathname === item.path ? 600 : 400,
                color: location.pathname === item.path ? 'var(--accent)' : 'var(--text)',
                fontSize: '0.9375rem',
              }}
            >
              {item.label}
            </Link>
          ))}
          <button
            onClick={handleLogout}
            style={{
              marginLeft: 'auto',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.9375rem',
              color: 'var(--text-secondary)',
              padding: '0 0.5rem',
            }}
          >
            Log out ({user.name})
          </button>
        </nav>
      )}
      <main className="page">{children}</main>
    </>
  );
}
