import { useState, useEffect } from 'react';
import { listRunways, getRunwayTimetable, createRunway, deleteRunway, updateRunway } from '../api/services';
import type { RunwayResponse, RunwayTimetableResponse, RunwayCreate } from '../types';

export default function RunwaysPage() {
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [selectedRunway, setSelectedRunway] = useState<string | null>(null);
  const [timetable, setTimetable] = useState<RunwayTimetableResponse | null>(null);
  const [capacity, setCapacity] = useState('');
  const [configuration, setConfiguration] = useState('');
  const [closureRunwayId, setClosureRunwayId] = useState('');
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

  const handleCreate = async () => {
    if (!capacity || !configuration) return;
    try {
      const data: RunwayCreate = { capacity: parseInt(capacity, 10), configuration };
      await createRunway(data);
      setCapacity('');
      setConfiguration('');
      fetchRunways();
    } catch {
      setError('Failed to create runway.');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteRunway(id);
      if (selectedRunway === id) { setSelectedRunway(null); setTimetable(null); }
      fetchRunways();
    } catch {
      setError('Failed to delete runway.');
    }
  };

  const handleViewTimetable = async (id: string) => {
    try {
      const res = await getRunwayTimetable(id);
      setTimetable(res.data);
      setSelectedRunway(id);
    } catch {
      setError('Failed to load timetable.');
    }
  };

  const handleCloseRunway = async () => {
    if (!closureRunwayId) return;
    try {
      // Mark runway as closed by updating its capacity to 0 (simple approach)
      await updateRunway(closureRunwayId, { capacity: 0 });
      setClosureRunwayId('');
      fetchRunways();
      setError('Runway closed successfully. Affected flights would be reassigned.');
    } catch {
      setError('Failed to close runway.');
    }
  };

  if (loading) return <div className="page"><p>Loading runways...</p></div>;

  return (
    <div className="page">
      <h1>Runway Management</h1>
      <p className="text-secondary">Manage runways, closures, and view timetables</p>

      {error && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#fff0f0' }}><p>{error}</p></div>}

      <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
        <div className="card" style={{ flex: 2, minWidth: 300, padding: '1.5rem' }}>
          <h2 className="section-title">All Runways</h2>
          {runways.length === 0 ? (
            <p className="text-secondary">No runways configured.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Capacity</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Configuration</th>
                  <th style={{ textAlign: 'right', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {runways.map(rw => (
                  <tr key={rw.id} style={{ borderBottom: '1px solid var(--border-light)', background: selectedRunway === rw.id ? 'var(--bg-secondary)' : 'transparent' }}>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{rw.id}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{rw.capacity > 0 ? rw.capacity : 'CLOSED'}</td>
                    <td style={{ padding: '0.75rem 0.5rem' }}>{rw.configuration}</td>
                    <td style={{ padding: '0.75rem 0.5rem', textAlign: 'right' }}>
                      <button className="secondary" onClick={() => handleViewTimetable(rw.id)} style={{ fontSize: '0.875rem', marginRight: '0.5rem' }}>Timetable</button>
                      <button className="secondary" onClick={() => handleDelete(rw.id)} style={{ fontSize: '0.875rem' }}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div style={{ flex: 1, minWidth: 280, display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card" style={{ padding: '1.5rem' }}>
            <h2 className="section-title">Add Runway</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '1rem' }}>
              <input
                placeholder="Capacity"
                value={capacity}
                onChange={e => setCapacity(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
              />
              <input
                placeholder="Configuration (e.g. 27L)"
                value={configuration}
                onChange={e => setConfiguration(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
              />
              <button className="primary" onClick={handleCreate}>Add Runway</button>
            </div>
          </div>

          <div className="card" style={{ padding: '1.5rem' }}>
            <h2 className="section-title">Close Runway</h2>
            <p className="text-secondary" style={{ fontSize: '0.875rem', marginBottom: '0.75rem' }}>
              Closing a runway will reassign affected flights.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <input
                placeholder="Runway ID to close"
                value={closureRunwayId}
                onChange={e => setClosureRunwayId(e.target.value)}
                style={{ padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
              />
              <button className="primary" onClick={handleCloseRunway} style={{ background: '#d32f2f' }}>Close Runway</button>
            </div>
          </div>
        </div>
      </div>

      {timetable && selectedRunway && (
        <div className="card" style={{ padding: '1.5rem', marginTop: '1.5rem' }}>
          <h2 className="section-title">Timetable for Runway {selectedRunway}</h2>
          {(!timetable.entries || timetable.entries.length === 0) ? (
            <p className="text-secondary">No entries for this runway.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Slot Time</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Flight Number</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Aircraft Type</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {timetable.entries.map((entry, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid var(--border-light)' }}>
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
