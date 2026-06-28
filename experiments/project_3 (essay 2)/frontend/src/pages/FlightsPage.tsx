import { useState, useEffect } from 'react';
import {
  listFlights, createFlight, updateFlight, deleteFlight,
} from '../api/services';
import type { FlightResponse, FlightCreate, FlightUpdate } from '../types';

const emptyForm: FlightCreate = {
  flightNumber: '', airline: '', origin: '', destination: '',
  scheduledTime: '', type: 'arrival',
};

export default function FlightsPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<FlightCreate>(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = () => {
    setLoading(true);
    listFlights()
      .then(data => setFlights(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (editingId !== null) {
        const upd: FlightUpdate = { ...form };
        Object.keys(upd).forEach(k => {
          if (upd[k as keyof FlightUpdate] === '') (upd as any)[k] = undefined;
        });
        await updateFlight(editingId, upd);
      } else {
        await createFlight(form);
      }
      setForm(emptyForm);
      setEditingId(null);
      await load();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const startEdit = (f: FlightResponse) => {
    setEditingId(f.id);
    setForm({
      flightNumber: f.flightNumber,
      airline: f.airline,
      origin: f.origin,
      destination: f.destination,
      scheduledTime: new Date(f.scheduledTime).toISOString().slice(0, 16),
      type: f.type,
    });
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this flight?')) return;
    try {
      await deleteFlight(id);
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <div className="page"><p>Loading flights...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <h1>Flight Management</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Register, edit, or cancel flights
      </p>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 className="section-title">{editingId ? 'Edit Flight' : 'Register New Flight'}</h2>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <input placeholder="Flight Number" value={form.flightNumber} onChange={e => setForm(p => ({ ...p, flightNumber: e.target.value }))} required />
          <input placeholder="Airline" value={form.airline} onChange={e => setForm(p => ({ ...p, airline: e.target.value }))} required />
          <input placeholder="Origin" value={form.origin} onChange={e => setForm(p => ({ ...p, origin: e.target.value }))} required />
          <input placeholder="Destination" value={form.destination} onChange={e => setForm(p => ({ ...p, destination: e.target.value }))} required />
          <input type="datetime-local" value={form.scheduledTime} onChange={e => setForm(p => ({ ...p, scheduledTime: e.target.value }))} required />
          <select value={form.type} onChange={e => setForm(p => ({ ...p, type: e.target.value }))}>
            <option value="arrival">Arrival</option>
            <option value="departure">Departure</option>
          </select>
          <div style={{ gridColumn: '1 / -1', display: 'flex', gap: '0.5rem' }}>
            <button type="submit" className="primary" disabled={saving}>
              {saving ? 'Saving...' : editingId ? 'Update Flight' : 'Register Flight'}
            </button>
            {editingId && (
              <button type="button" className="secondary" onClick={() => { setEditingId(null); setForm(emptyForm); }}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <h2 className="section-title">All Flights ({flights.length})</h2>
        {flights.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No flights registered yet.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Flight#</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Airline</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Origin → Dest</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Time</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Type</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {flights.map(f => (
                  <tr key={f.id}>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)', fontWeight: 600 }}>{f.flightNumber}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{f.airline}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{f.origin} → {f.destination}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{new Date(f.scheduledTime).toLocaleString()}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>
                      <span style={{
                        padding: '0.125rem 0.5rem', borderRadius: 'var(--radius-s)', fontSize: '0.8rem', fontWeight: 600,
                        background: f.type === 'arrival' ? 'rgba(52,199,89,0.15)' : 'rgba(255,159,10,0.15)',
                        color: f.type === 'arrival' ? 'var(--success)' : 'var(--warning)',
                      }}>{f.type}</span>
                    </td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>
                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem' }} onClick={() => startEdit(f)}>Edit</button>
                        <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem', color: 'var(--danger)' }} onClick={() => handleDelete(f.id)}>Delete</button>
                      </div>
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
