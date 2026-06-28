
import { NavLink } from 'react-router-dom';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <nav>
        <NavLink to="/" style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--text)', textDecoration: 'none' }}>
          🩸 Blood Bank
        </NavLink>
        <NavLink to="/" end style={({ isActive }) => ({ color: isActive ? 'var(--accent)' : 'var(--text-secondary)', textDecoration: 'none', fontWeight: isActive ? 600 : 400 })}>
          Dashboard
        </NavLink>
        <NavLink to="/blood-units" style={({ isActive }) => ({ color: isActive ? 'var(--accent)' : 'var(--text-secondary)', textDecoration: 'none', fontWeight: isActive ? 600 : 400 })}>
          Blood Units
        </NavLink>
        <NavLink to="/transfusion-requests" style={({ isActive }) => ({ color: isActive ? 'var(--accent)' : 'var(--text-secondary)', textDecoration: 'none', fontWeight: isActive ? 600 : 400 })}>
          Transfusion Requests
        </NavLink>
        <NavLink to="/reservations" style={({ isActive }) => ({ color: isActive ? 'var(--accent)' : 'var(--text-secondary)', textDecoration: 'none', fontWeight: isActive ? 600 : 400 })}>
          Reservations
        </NavLink>
      </nav>
      <main>{children}</main>
    </div>
  );
}
