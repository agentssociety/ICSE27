
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { slotApi, createStandardSlot } from '../api/services';
import type { SlotResponse } from '../types';

export default function SlotsPage() {
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [startTime, setStartTime] = useState('');
  const [flightType, setFlightType] = useState<'arrival' | 'departure' | 'emergency' | ''>('');
  const [error, setError] = useState('');

  const fetchSlots = () => {
    setLoading(true);
    slotApi.getAll()
      .then(setSlots)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(fetchSlots, []);

  const handleCreateSlot = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await createStandardSlot({
        startTime,
        flight_type: flightType || undefined,
      });
      setShowForm(false);
      setStartTime('');
      setFlightType('');
      fetchSlots();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to create slot');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this slot?')) return;
    try {
      await slotApi.delete(id);
      fetchSlots();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to delete slot');
    }
  };

  return (
    <Layout>
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h1>Slots</h1>
          <button className="primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : '+ Allocate Slot'}
          </button>
        </div>

        {error && (
          <div className="card" style={{ background: '#fff5f5', borderColor: 'var(--danger)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        {showForm && (
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 className="section-title">Allocate 5-Minute Slot</h3>
            <form onSubmit={handleCreateSlot} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Start Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={startTime}
                    onChange={e => setStartTime(e.target.value)}
                  />
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.25rem' }}>Slot will be 5 min with 3 min gap after</p>
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Flight Type</label>
                  <select value={flightType} onChange={e => setFlightType(e.target.value as any)}>
                    <option value="">Regular</option>
                    <option value="arrival">Arrival</option>
                    <option value="departure">Departure</option>
                    <option value="emergency">Emergency</option>
                  </select>
                </div>
              </div>
              <div>
                <button type="submit" className="primary">Allocate Slot</button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading slots...</p>
        ) : slots.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No slots allocated yet.</p>
          </div>
        ) : (
          <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)', color: 'var(--text-secondary)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Start Time</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>End Time</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Duration</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Type</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Gap After</th>
                  <th style={{ textAlign: 'right', padding: '0.75rem 1rem' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {slots.map(s => {
                  const isEmergency = s.flight_type === 'emergency';
                  return (
                    <tr key={s.id} style={{
                      borderTop: '1px solid var(--border-light)',
                      background: isEmergency ? '#fff5f5' : undefined,
                    }}>
                      <td style={{ padding: '0.75rem 1rem' }}>{s.id}</td>
                      <td style={{ padding: '0.75rem 1rem' }}>{new Date(s.startTime).toLocaleString()}</td>
                      <td style={{ padding: '0.75rem 1rem' }}>{new Date(s.endTime).toLocaleString()}</td>
                      <td style={{ padding: '0.75rem 1rem' }}>{s.duration}</td>
                      <td style={{ padding: '0.75rem 1rem' }}>
                        {isEmergency ? (
                          <span className="badge" style={{ background: 'var(--danger)', color: '#fff' }}>Emergency</span>
                        ) : s.flight_type === 'arrival' ? (
                          <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>Arrival</span>
                        ) : s.flight_type === 'departure' ? (
                          <span className="badge" style={{ background: 'var(--warning)', color: '#fff' }}>Departure</span>
                        ) : (
                          <span className="badge">Regular</span>
                        )}
                      </td>
                      <td style={{ padding: '0.75rem 1rem' }}>{s.gapAfter}</td>
                      <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                        <button className="secondary" style={{ fontSize: '0.75rem' }} onClick={() => handleDelete(s.id)}>Delete</button>
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
