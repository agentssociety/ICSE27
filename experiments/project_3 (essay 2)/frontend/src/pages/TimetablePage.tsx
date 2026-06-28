import { useState, useEffect } from 'react';
import { listSlots, listFlights, listRunways, listTimeSlots } from '../api/services';
import type { SlotResponse, FlightResponse, RunwayResponse, TimeSlotResponse } from '../types';

export default function TimetablePage() {
  const [slots, setSlots] = useState<SlotResponse[]>([]);
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [timeSlots, setTimeSlots] = useState<TimeSlotResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRunway, setFilterRunway] = useState('');

  useEffect(() => {
    setLoading(true);
    Promise.all([listSlots(), listFlights(), listRunways(), listTimeSlots()])
      .then(([s, f, r, t]) => {
        setSlots(s);
        setFlights(f);
        setRunways(r);
        setTimeSlots(t);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const getFlight = (id?: number) => flights.find(f => f.id === id);
  const getRunway = (id?: number) => runways.find(r => r.id === id);
  const getTimeSlot = (id?: number) => timeSlots.find(t => t.flight_id === id);

  const filteredRunways = filterRunway
    ? runways.filter(r => r.runwayId.toLowerCase().includes(filterRunway.toLowerCase()))
    : runways;

  if (loading) return <div className="page"><p>Loading timetable...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <h1>Runway Slot Timetable</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        View all allocated slots with delay and emergency indicators
      </p>

      <div style={{ marginBottom: '1.5rem', maxWidth: 300 }}>
        <input
          placeholder="Filter by runway..."
          value={filterRunway}
          onChange={e => setFilterRunway(e.target.value)}
        />
      </div>

      {filteredRunways.length === 0 ? (
        <p style={{ color: 'var(--text-secondary)' }}>No runways found.</p>
      ) : (
        filteredRunways.map(runway => {
          const runwaySlots = slots.filter(s => s.runway_id === runway.id);
          return (
            <div className="card" key={runway.id} style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 className="section-title" style={{ marginBottom: 0 }}>
                  {runway.runwayId}
                </h2>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  {runway.length}m
                </span>
              </div>

              {runwaySlots.length === 0 ? (
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>No slots allocated.</p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {runwaySlots.map(slot => {
                    const flight = getFlight(slot.flight_id);
                    const timeSlot = getTimeSlot(slot.flight_id);
                    return (
                      <div key={slot.id} style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '0.75rem 1rem',
                        background: 'var(--bg-secondary)',
                        borderRadius: 'var(--radius-s)',
                        fontSize: '0.9rem',
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          <span style={{ fontWeight: 600, minWidth: 80 }}>
                            {flight?.flightNumber || ('Flight #' + slot.flight_id)}
                          </span>
                          <span style={{ color: 'var(--text-secondary)' }}>
                            {flight?.origin} → {flight?.destination}
                          </span>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                          {flight && (
                            <span style={{
                              padding: '0.125rem 0.5rem',
                              borderRadius: 'var(--radius-s)',
                              fontSize: '0.8rem',
                              fontWeight: 600,
                              background: flight.type === 'arrival' ? 'rgba(52,199,89,0.15)' : 'rgba(255,159,10,0.15)',
                              color: flight.type === 'arrival' ? 'var(--success)' : 'var(--warning)',
                            }}>
                              {flight.type}
                            </span>
                          )}
                          <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                            Slot #{slot.id}
                          </span>
                          <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                            {flight && new Date(flight.scheduledTime).toLocaleTimeString()}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
