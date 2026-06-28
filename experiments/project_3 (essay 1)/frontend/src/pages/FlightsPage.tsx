import { useState, useEffect } from 'react';
import { listFlights, createFlight, deleteFlight } from '../api/services';
import type { FlightResponse, FlightCreate } from '../types';

export default function FlightsPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [flightNumber, setFlightNumber] = useState('');
  const [aircraftType, setAircraftType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchFlights = async () => {
    try {
      const res = await listFlights();
      setFlights(res.data);
      setLoading(false);
    } catch {
      setError('Failed to load flights.');
      setLoading(false);
    }
  };

  useEffect(() => { fetchFlights(); }, []);

  const handleCreate = async () => {
    if (!flightNumber || !aircraftType) return;
    try {
      const data: FlightCreate = { flightNumber, aircraftType };
      await createFlight(data);
      setFlightNumber('');
      setAircraftType('');
      fetchFlights();
    } catch {
      setError('Failed to create flight.');
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteFlight(id);
      fetchFlights();
    } catch {
      setError('Failed to delete flight.');
    }
  };

  if (loading) return <div className="page"><p>Loading flights...</p></div>;

  return (
    <div className="page">
      <h1>Flight Registration</h1>
      <p className="text-secondary">Register incoming and outgoing flights</p>

      {error && <div className="card" style={{ padding: '1rem', marginBottom: '1rem', background: '#fff0f0' }}><p>{error}</p></div>}

      <div className="card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
        <h2 className="section-title">New Flight</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1rem' }}>
          <input
            placeholder="Flight Number (e.g. AA123)"
            value={flightNumber}
            onChange={e => setFlightNumber(e.target.value)}
            style={{ flex: 1, minWidth: 180, padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
          />
          <input
            placeholder="Aircraft Type (e.g. Boeing 737)"
            value={aircraftType}
            onChange={e => setAircraftType(e.target.value)}
            style={{ flex: 1, minWidth: 180, padding: '0.5rem 0.75rem', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-m)', fontSize: '1rem' }}
          />
          <button className="primary" onClick={handleCreate}>Register Flight</button>
        </div>
      </div>

      <div className="card" style={{ padding: '1.5rem' }}>
        <h2 className="section-title">Aircraft Movement Log</h2>
        {flights.length === 0 ? (
          <p className="text-secondary">No flights registered yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>ID</th>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Flight Number</th>
                <th style={{ textAlign: 'left', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Aircraft Type</th>
                <th style={{ textAlign: 'right', padding: '0.75rem 0.5rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {flights.map(flight => (
                <tr key={flight.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{flight.id}</td>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{flight.flightNumber}</td>
                  <td style={{ padding: '0.75rem 0.5rem' }}>{flight.aircraftType}</td>
                  <td style={{ padding: '0.75rem 0.5rem', textAlign: 'right' }}>
                    <button className="secondary" onClick={() => handleDelete(flight.id)} style={{ fontSize: '0.875rem' }}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
