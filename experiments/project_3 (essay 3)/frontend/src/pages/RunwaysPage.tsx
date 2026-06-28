
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { runwayApi, flightApi, closeRunway } from '../api/services';
import type { RunwayResponse, FlightResponse } from '../types';

export default function RunwaysPage() {
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCloseForm, setShowCloseForm] = useState(false);
  const [selectedRunway, setSelectedRunway] = useState('');
  const [alternateRunway, setAlternateRunway] = useState('');
  const [showTimetable, setShowTimetable] = useState(false);
  const [timetableRunway, setTimetableRunway] = useState('');
  const [error, setError] = useState('');

  const fetchData = () => {
    setLoading(true);
    Promise.all([
      runwayApi.getAll(),
      flightApi.getAll(),
    ])
      .then(([r, f]) => {
        setRunways(r);
        setFlights(f);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(fetchData, []);

  const handleCloseRunway = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const result = await closeRunway(selectedRunway, alternateRunway);
      setShowCloseForm(false);
      setSelectedRunway('');
      setAlternateRunway('');
      fetchData();
      alert(`Runway closed. ${result.reassignedFlights.length} flights reassigned.`);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to close runway');
    }
  };

  return (
    <Layout>
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h1>Runways</h1>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="secondary" onClick={() => setShowTimetable(!showTimetable)}>
              {showTimetable ? 'Hide Timetable' : 'View Timetable'}
            </button>
            <button className="primary" onClick={() => setShowCloseForm(!showCloseForm)}>
              {showCloseForm ? 'Cancel' : 'Close Runway'}
            </button>
          </div>
        </div>

        {error && (
          <div className="card" style={{ background: '#fff5f5', borderColor: 'var(--danger)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        {/* Close Runway Form */}
        {showCloseForm && (
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 className="section-title">Close Runway & Reassign Flights</h3>
            <form onSubmit={handleCloseRunway} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Runway to Close</label>
                  <select required value={selectedRunway} onChange={e => setSelectedRunway(e.target.value)}>
                    <option value="">Select runway...</option>
                    {runways.map(r => (
                      <option key={r.id} value={r.id}>{r.id}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Alternate Runway</label>
                  <select required value={alternateRunway} onChange={e => setAlternateRunway(e.target.value)}>
                    <option value="">Select alternate...</option>
                    {runways.filter(r => r.id !== selectedRunway).map(r => (
                      <option key={r.id} value={r.id}>{r.id}</option>
                    ))}
                  </select>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.25rem' }}>
                    Flights delayed &gt;60 min will be marked delayed
                  </p>
                </div>
              </div>
              <div>
                <button type="submit" className="primary">Close Runway & Reassign</button>
              </div>
            </form>
          </div>
        )}

        {/* Timetable View */}
        {showTimetable && (
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 className="section-title">Runway Slot Timetable</h3>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Select Runway</label>
              <select value={timetableRunway} onChange={e => setTimetableRunway(e.target.value)} style={{ maxWidth: '300px' }}>
                <option value="">All runways</option>
                {runways.map(r => (
                  <option key={r.id} value={r.id}>{r.id}</option>
                ))}
              </select>
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)', color: 'var(--text-secondary)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Flight ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Runway</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Flight Number</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Est. Departure</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {flights.length === 0 ? (
                  <tr>
                    <td colSpan={5} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                      No flights scheduled.
                    </td>
                  </tr>
                ) : (
                  flights.map(f => {
                    const isDelayed = f.estimatedDepartureTime && (Date.now() - new Date(f.estimatedDepartureTime).getTime()) > 60 * 60 * 1000;
                    const runway = runways.find(r => r.flight_id === f.id);
                    if (timetableRunway && runway?.id !== timetableRunway) return null;

                    let status = 'On-Time';
                    let statusColor = 'var(--success)';
                    if (isDelayed) {
                      status = 'Delayed';
                      statusColor = 'var(--warning)';
                    }
                    if (runway?.id === selectedRunway && showCloseForm) {
                      status = 'Reassigning';
                      statusColor = 'var(--accent)';
                    }

                    return (
                      <tr key={f.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                        <td style={{ padding: '0.75rem 1rem' }}>{f.id}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>{runway?.id || '—'}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>{f.flightNumber}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>{new Date(f.estimatedDepartureTime).toLocaleString()}</td>
                        <td style={{ padding: '0.75rem 1rem' }}>
                          <span className="badge" style={{ background: statusColor, color: statusColor === 'var(--text-secondary)' ? undefined : '#fff' }}>
                            {status}
                          </span>
                        </td>
                      </tr>
                    );
                  }).filter(Boolean)
                )}
              </tbody>
            </table>
          </div>
        )}

        {/* Runway List */}
        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading runways...</p>
        ) : runways.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No runways configured.</p>
          </div>
        ) : (
          <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)', color: 'var(--text-secondary)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Runway ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Assigned Flight</th>
                  <th style={{ textAlign: 'right', padding: '0.75rem 1rem' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {runways.map(r => {
                  const assignedFlight = flights.find(f => f.id === r.flight_id);
                  return (
                    <tr key={r.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                      <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>{r.id}</td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        {assignedFlight ? `${assignedFlight.flightNumber} (#${assignedFlight.id})` : '—'}
                      </td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                        <button className="secondary" style={{ fontSize: '0.75rem' }} onClick={() => {
                          setSelectedRunway(r.id);
                          setShowCloseForm(true);
                        }}>
                          Close
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}
