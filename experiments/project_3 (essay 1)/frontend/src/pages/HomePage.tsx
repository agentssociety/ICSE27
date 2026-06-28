import { useState, useEffect } from 'react';
import { listFlights } from '../api/services';
import { listRunways } from '../api/services';
import { listSlots } from '../api/services';
import type { FlightResponse, RunwayResponse, SlotResponse } from '../types';

export default function HomePage() {
  const [flightCount, setFlightCount] = useState(0);
  const [runwayCount, setRunwayCount] = useState(0);
  const [slotCount, setSlotCount] = useState(0);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [flights, runways, slots] = await Promise.all([
          listFlights(),
          listRunways(),
          listSlots(),
        ]);
        setFlightCount(flights.data.length);
        setRunwayCount(runways.data.length);
        setSlotCount(slots.data.length);
      } catch {
        setError('Failed to load dashboard data. Backend may be unavailable.');
      }
    };
    fetchStats();
  }, []);

  if (error) {
    return (
      <div className="page">
        <div className="card" style={{ padding: '2rem', textAlign: 'center' }}>
          <p className="text-secondary">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <h1>Airport Runway Scheduling</h1>
      <p className="text-secondary">Dashboard overview</p>
      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
        <div className="card" style={{ flex: 1, minWidth: 180, padding: '1.5rem' }}>
          <h2 className="section-title">Flights</h2>
          <p style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--accent)' }}>{flightCount}</p>
        </div>
        <div className="card" style={{ flex: 1, minWidth: 180, padding: '1.5rem' }}>
          <h2 className="section-title">Runways</h2>
          <p style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--accent)' }}>{runwayCount}</p>
        </div>
        <div className="card" style={{ flex: 1, minWidth: 180, padding: '1.5rem' }}>
          <h2 className="section-title">Slots</h2>
          <p style={{ fontSize: '2rem', fontWeight: 600, color: 'var(--accent)' }}>{slotCount}</p>
        </div>
      </div>
    </div>
  );
}
