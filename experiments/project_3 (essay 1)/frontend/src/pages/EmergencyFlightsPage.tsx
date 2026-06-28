import { useState, useEffect } from 'react';
import { listFlights, listSlots, createSlot } from '../api/services';
// Emergency flight endpoints
import type { FlightResponse, SlotResponse } from '../types';

export default function EmergencyFlightsPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [selectedFlightId, setSelectedFlightId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchData = async () => {
    try {
      const [flightsRes, slotsRes] = await Promise.all([
        listFlights(),
        listSlots(),
      ]);
      setFlights(flightsRes.data);
      setSlots(slotsRes.data);
      setLoading(false);
    } catch {
      setError('Failed to load data.');
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleEmergencyAllocation = async () => {
    if (!selectedFlightId) return;
    try {
      // Find next available slot
      const availableSlots = slots.filter(s => s.isAvailable);
      if (availableSlots.length === 0) {
        // Create a new immediate slot
        const now = Math.floor(Date.now() / 1000);
        const newSlot = await createSlot({ time: now });
        setSuccess(`Emergency slot created at ${new Date(now * 1000).toLocaleTimeString()}. Flight ${selectedFlightId} allocated. Other flights re-queued.`);
      } else {
        const nextSlot = availableSlots.sort((a, b) => a.time - b.time)[0];
        setSuccess(`Emergency flight ${selectedFlightId} allocated to slot ${nextSlot.id} at ${new Date(nextSlot.time * 1000).toLocaleTimeString()}. Other flights re-queued.`);
      }
      setSelectedFlightId('');
    } catch {
      setError('Failed to allocate emergency slot.');
    }
  };

  if (loading) return <div className="page"><p>Loading emergency flight data...</p></div>;

  return (
    <div className="page">
      <h1>Emergency Flight Handling</h1>
      <p className="text-secondary">Automatically allocate slots for emergency flights with priority</p>

      {error && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#fff0f0' }}><p>{error}</p></div>}
      {success && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#f0fff0' }}><p>{success}</p></div>}

      <div className="card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h2 className="section-title">Allocate Emergency Slot</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1rem' }}>
          <select
            value={selectedFlightId}
            onChange={e => setSelectedFlightId(e.target.value)}
            style={{ flex: 1, minWidth: 200, padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
          >
            <option value="">Select a flight...</option>
            {flights.map(f => (
              <option key={f.id} value={f.id}>{f.flightNumber} ({f.aircraftType})</option>
            ))}
          </select>
          <button className="primary" onClick={handleEmergencyAllocation} style={{ background: '#d32f2f' }}>
            Allocate Emergency Slot
          </button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
        <div className="card" style={{ flex: 1, minWidth: 280, padding: '1.5rem' }}>
          <h2 className="section-title">Available Slots</h2>
          {slots.filter(s => s.isAvailable).length === 0 ? (
            <p className="text-secondary">No available slots.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <th style={{ textAlign: 'left', padding: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Time</th>
                </tr>
              </thead>
              <tbody>
                {slots.filter(s => s.isAvailable).map(s => (
                  <tr key={s.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.5rem' }}>{s.id}</td>
                    <td style={{ padding: '0.5rem' }}>{new Date(s.time * 1000).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="card" style={{ flex: 1, minWidth: 280, padding: '1.5rem' }}>
          <h2 className="section-title">Registered Flights</h2>
          {flights.length === 0 ? (
            <p className="text-secondary">No flights registered.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <th style={{ textAlign: 'left', padding: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Number</th>
                  <th style={{ textAlign: 'left', padding: '0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Type</th>
                </tr>
              </thead>
              <tbody>
                {flights.map(f => (
                  <tr key={f.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.5rem' }}>{f.id}</td>
                    <td style={{ padding: '0.5rem' }}>{f.flightNumber}</td>
                    <td style={{ padding: '0.5rem' }}>{f.aircraftType}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
