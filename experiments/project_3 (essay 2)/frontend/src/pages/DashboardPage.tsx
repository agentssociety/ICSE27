import { useState, useEffect } from 'react';
import { listFlights } from '../api/services';
import type { FlightResponse } from '../types';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listFlights()
      .then(data => setFlights(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const arrivals = flights.filter(f => f.type === 'arrival');
  const departures = flights.filter(f => f.type === 'departure');

  if (loading) return <div className="page"><p>Loading dashboard...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Air traffic control overview
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3>Total Flights</h3>
          <p style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--accent)' }}>{flights.length}</p>
        </div>
        <div className="card">
          <h3>Arrivals</h3>
          <p style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--success)' }}>{arrivals.length}</p>
        </div>
        <div className="card">
          <h3>Departures</h3>
          <p style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--warning)' }}>{departures.length}</p>
        </div>
      </div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="section-title" style={{ marginBottom: 0 }}>Recent Flights</h2>
          <Link to="/flights"><button className="secondary">View All</button></Link>
        </div>
        {flights.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No flights registered yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Flight</th>
                <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Airline</th>
                <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Route</th>
                <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Time</th>
                <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Type</th>
              </tr>
            </thead>
            <tbody>
              {flights.slice(0, 10).map(f => (
                <tr key={f.id}>
                  <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)', fontWeight: 600 }}>{f.flightNumber}</td>
                  <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{f.airline}</td>
                  <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{f.origin} → {f.destination}</td>
                  <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{new Date(f.scheduledTime).toLocaleTimeString()}</td>
                  <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>
                    <span style={{
                      padding: '0.125rem 0.5rem',
                      borderRadius: 'var(--radius-s)',
                      fontSize: '0.8rem',
                      fontWeight: 600,
                      background: f.type === 'arrival' ? 'rgba(52,199,89,0.15)' : 'rgba(255,159,10,0.15)',
                      color: f.type === 'arrival' ? 'var(--success)' : 'var(--warning)',
                    }}>
                      {f.type}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
