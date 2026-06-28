import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="page">
      <div className="card" style={{ textAlign: 'center' }}>
        <h1>Triage Queue System</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
          Manage patient intake, triage, and queue prioritization.
        </p>
        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <Link to="/register">
            <button className="primary">Register New Patient</button>
          </Link>
          <Link to="/queue">
            <button className="secondary">View Queue</button>
          </Link>
          <Link to="/dashboard">
            <button className="secondary">Live Dashboard</button>
          </Link>
        </div>
      </div>
    </div>
  );
}
