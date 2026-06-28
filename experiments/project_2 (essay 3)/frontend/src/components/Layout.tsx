import { NavLink } from 'react-router-dom';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/blood-units">Blood Units</NavLink>
        <NavLink to="/transfusion-requests">Requests</NavLink>
        <NavLink to="/reservations">Reservations</NavLink>
      </nav>
      {children}
    </>
  );
}
