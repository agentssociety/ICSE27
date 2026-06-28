
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { flightApi, slotApi, runwayApi } from '../api/services';
import type { FlightResponse, SlotResponse, RunwayResponse } from '../types';

export default function DashboardPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      flightApi.getAll(),
      slotApi.getAll(),
      runwayApi.getAll(),
    ])
      .then(([f, s, r]) => {
        setFlights(f);
        setSlots(s);
        setRunways(r);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <Layout>
      <div className="page"><p>Loading dashboard...</p></div>
    </Layout>
  );

  const emergencyCount = slots.filter(s => s.flight_type === 'emergency').length;
  const delayedFlights = flights.filter(f => {
    if (!f.estimatedDepartureTime) return false;
    const scheduled = new Date(f.estimatedDepartureTime).getTime();
    const now = Date.now();
    return (now - scheduled) > 60 * 60 * 1000;
  }).length;

  return (
    <Layout>
      <div className="page">
        <h1 style={{ marginBottom: '1.5rem' }}>Dashboard</h1>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent)' }}>{flights.length}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Total Flights</div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent)' }}>{slots.length}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Total Slots</div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--success)' }}>{runways.length}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Runways</div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: emergencyCount > 0 ? 'var(--danger)' : 'var(--success)' }}>{emergencyCount}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Emergency Slots</div>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: delayedFlights > 0 ? 'var(--warning)' : 'var(--success)' }}>{delayedFlights}</div>
            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Delayed Flights</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div className="card">
            <h3 className="section-title">Recent Flights</h3>
            {flights.length === 0 ? (
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>No flights registered yet.</p>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
                <thead>
                  <tr style={{ color: 'var(--text-secondary)', borderBottom: '1px solid var(--border-light)' }}>
                    <th style={{ textAlign: 'left', padding: '0.5rem 0' }}>Flight</th>
                    <th style={{ textAlign: 'left', padding: '0.5rem 0' }}>Origin</th>
                    <th style={{ textAlign: 'left', padding: '0.5rem 0' }}>Destination</th>
                  </tr>
                </thead>
                <tbody>
                  {flights.slice(0, 5).map(f => (
                    <tr key={f.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                      <td style={{ padding: '0.5rem 0' }}>{f.flightNumber}</td>
                      <td style={{ padding: '0.5rem 0' }}>{f.origin}</td>
                      <td style={{ padding: '0.5rem 0' }}>{f.destination}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div className="card">
            <h3 className="section-title">Runway Overview</h3>
            {runways.length === 0 ? (
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>No runways configured.</p>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
                <thead>
                  <tr style={{ color: 'var(--text-secondary)', borderBottom: '1px solid var(--border-light)' }}>
                    <th style={{ textAlign: 'left', padding: '0.5rem 0' }}>Runway ID</th>
                    <th style={{ textAlign: 'left', padding: '0.5rem 0' }}>Flight Assigned</th>
                  </tr>
                </thead>
                <tbody>
                  {runways.slice(0, 5).map(r => (
                    <tr key={r.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                      <td style={{ padding: '0.5rem 0' }}>{r.id}</td>
                      <td style={{ padding: '0.5rem 0' }}>{r.flight_id ? `Flight #${r.flight_id}` : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}
