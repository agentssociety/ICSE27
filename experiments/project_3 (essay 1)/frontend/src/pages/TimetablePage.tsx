import { useState, useEffect } from 'react';
import { listRunways, getRunwayTimetable } from '../api/services';
import type { RunwayResponse, RunwayTimetableResponse } from '../types';

export default function TimetablePage() {
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [selectedRunway, setSelectedRunway] = useState('');
  const [timetable, setTimetable] = useState<RunwayTimetableResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchRunways = async () => {
    try {
      const res = await listRunways();
      setRunways(res.data);
      setLoading(false);
    } catch {
      setError('Failed to load runways.');
      setLoading(false);
    }
  };

  useEffect(() => { fetchRunways(); }, []);

  const handleSelectRunway = async (id: string) => {
    setSelectedRunway(id);
    try {
      const res = await getRunwayTimetable(id);
      setTimetable(res.data);
    } catch {
      setError('Failed to load timetable.');
    }
  };

  if (loading) return <div className="page"><p>Loading...</p></div>;

  return (
    <div className="page">
      <h1>Runway Slot Timetable</h1>
      <p className="text-secondary">View allocated time slots, flight details, and status per runway</p>

      {error && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#fff0f0' }}><p>{error}</p></div>}

      <div className="card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h2 className="section-title">Select Runway</h2>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '1rem' }}>
          {runways.map(rw => (
            <button
              key={rw.id}
              className={selectedRunway === rw.id ? 'primary' : 'secondary'}
              onClick={() => handleSelectRunway(rw.id)}
            >
              {rw.id} ({rw.configuration})
            </button>
          ))}
        </div>
      </div>

      {timetable && (
        <div className="card" style={{ padding: '1.5rem' }}>
          <h2 className="section-title">Timetable — {timetable.runway_id}</h2>
          <p className="text-secondary">Status: {timetable.runway_status ?? 'Unknown'}</p>

          {!timetable.entries || timetable.entries.length === 0 ? (
            <p className="text-secondary" style={{ marginTop: '1rem' }}>No scheduled flights for this runway.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Slot ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Time</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Flight Number</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Aircraft</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {timetable.entries.map((entry, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{entry.slot_id ?? '-'}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{entry.slot_time ? new Date(entry.slot_time * 1000).toLocaleString() : '-'}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{entry.flight_number ?? '-'}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{entry.aircraft_type ?? '-'}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{entry.status ?? '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}
