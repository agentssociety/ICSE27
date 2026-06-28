import { Link, useLocation } from 'react-router-dom';

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  const isActive = (path: string) =>
    location.pathname === path ? { opacity: 1, fontWeight: 600 } : {};

  return (
    <>
      <nav>
        <Link to="/" style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--text)', marginRight: '0.5rem' }}>
          Queue Manager
        </Link>
        <Link to="/" style={isActive('/')}>Dashboard</Link>
        <Link to="/register" style={isActive('/register')}>Register</Link>
        <Link to="/assign-urgency" style={isActive('/assign-urgency')}>Assign Urgency</Link>
        <Link to="/dequeue" style={isActive('/dequeue')}>Dequeue</Link>
      </nav>
      <main>{children}</main>
    </>
  );
}
