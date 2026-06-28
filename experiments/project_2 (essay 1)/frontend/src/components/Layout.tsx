import { Link } from "react-router-dom";

const Layout = () => {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/blood-units">Blood Units</Link>
      <Link to="/transfusion-requests">Transfusion Requests</Link>
      <Link to="/reservations">Reservations</Link>
      <Link to="/dashboard">Dashboard</Link>
    </nav>
  );
};

export default Layout;
