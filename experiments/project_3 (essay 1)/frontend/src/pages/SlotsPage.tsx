import { useState, useEffect } from 'react';
import { listSlots, createSlot } from '../api/services';
import type { SlotResponse, SlotCreate } from '../types';

export default function SlotsPage() {
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [time, setTime] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchSlots = async () => {
    try {
      const res = await listSlots();
      setSlots(res.data);
      setLoading(false);
    } catch {
      setError('Failed to load slots.');
      setLoading(false);
    }
  };

  useEffect(() => { fetchSlots(); }, []);

  const handleCreate = async () => {
    if (!time) return;
    try {
      const data: SlotCreate = { time: parseInt(time, 10) };
      await createSlot(data);
      setTime('');
      fetchSlots();
    } catch {
      setError('Failed to create slot.');
    }
  };

  if (loading) return <div className="page"><p>Loading slots...</p></div>;

  return (
    <div className="page">
      <h1>Slot Allocation</h1>
      <p className="text-secondary">Manage time slots for flights (5-minute slots with 3-minute gaps)</p>

      {error && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#fff0f0' }}><p>{error}</p></div>}

      <div className="card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h2 className="section-title">Create New Slot</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1rem' }}>
          <input
            placeholder="Slot time (unix timestamp)"
            value={time}
            onChange={e => setTime(e.target.value)}
            style={{ flex: 1, minWidth: 180, padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
          />
          <button className="primary" onClick={handleCreate}>Create Slot</button>
        </div>
      </div>

      <div className="card" style={{ padding: '1.5rem' }}>
        <h2 className="section-title">All Slots</h2>
        {slots.length === 0 ? (
          <p className="text-secondary">No slots created yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>ID</th>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Time</th>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Available</th>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Resource ID</th>
              </tr>
            </thead>
            <tbody>
              {slots.map(slot => (
                <tr key={slot.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{slot.id}</td>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{new Date(slot.time * 1000).toLocaleString()}</td>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{slot.isAvailable ? 'Yes' : 'No'}</td>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{slot.resource_id ?? '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
