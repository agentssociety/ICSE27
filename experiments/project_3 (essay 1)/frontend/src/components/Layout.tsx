import { NavLink, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <>
      <nav>
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/flights">Flight Registration</NavLink>
        <NavLink to="/slots">Slot Allocation</NavLink>
        <NavLink to="/runways">Runway Management</NavLink>
        <NavLink to="/emergency">Emergency Flights</NavLink>
        <NavLink to="/timetable">Timetable</NavLink>
      </nav>
      <main className="page">
        <Outlet />
      </main>
    </>
  );
}
