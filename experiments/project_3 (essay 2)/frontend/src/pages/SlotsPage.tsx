import { useState, useEffect } from 'react';
import { listSlots, createSlot, deleteSlot, listFlights, listRunways } from '../api/services';
import type { SlotResponse, FlightResponse, RunwayResponse } from '../types';

export default function SlotsPage() {
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [flightId, setFlightId] = useState('');
  const [runwayId, setRunwayId] = useState('');

  const load = async () => {
    setLoading(true);
    try {
      const [s, f, r] = await Promise.all([listSlots(), listFlights(), listRunways()]);
      setSlots(s);
      setFlights(f);
      setRunways(r);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createSlot({
        flight_id: flightId ? parseInt(flightId) : undefined,
        runway_id: runwayId ? parseInt(runwayId) : undefined,
      });
      setFlightId('');
      setRunwayId('');
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this slot?')) return;
    try {
      await deleteSlot(id);
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getFlightLabel = (id?: number) => {
    const f = flights.find(f => f.id === id);
    return f ? `${f.flightNumber} (${f.airline})` : `Flight #${id}`;
  };

  const getRunwayLabel = (id?: number) => {
    const r = runways.find(r => r.id === id);
    return r ? r.runwayId : `Runway #${id}`;
  };

  if (loading) return <div className="page"><p>Loading slots...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <h1>Slot Allocation</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Manage time slot assignments for flights
      </p>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 className="section-title">Create New Slot</h2>
        <form onSubmit={handleCreate} style={{ display: 'flex', gap: '1rem', alignItems: 'end', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 200 }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Flight</label>
            <select value={flightId} onChange={e => setFlightId(e.target.value)}>
              <option value="">-- Select flight --</option>
              {flights.map(f => (
                <option key={f.id} value={f.id}>{f.flightNumber} - {f.airline}</option>
              ))}
            </select>
          </div>
          <div style={{ flex: 1, minWidth: 200 }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Runway</label>
            <select value={runwayId} onChange={e => setRunwayId(e.target.value)}>
              <option value="">-- Select runway --</option>
              {runways.map(r => (
                <option key={r.id} value={r.id}>{r.runwayId}</option>
              ))}
            </select>
          </div>
          <button type="submit" className="primary">Create Slot</button>
        </form>
      </div>

      <div className="card">
        <h2 className="section-title">All Slots ({slots.length})</h2>
        {slots.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No slots allocated yet.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>ID</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Flight</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Runway</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {slots.map(s => (
                  <tr key={s.id}>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)', fontWeight: 600 }}>{s.id}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{getFlightLabel(s.flight_id)}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{getRunwayLabel(s.runway_id)}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>
                      <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem', color: 'var(--danger)' }} onClick={() => handleDelete(s.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
