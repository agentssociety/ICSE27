
import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { flightApi } from '../api/services';
import type { FlightResponse, FlightCreate } from '../types';

export default function FlightsPage() {
  const [flights, setFlights] = useState<FlightResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<FlightCreate>({
    flightNumber: '',
    origin: '',
    destination: '',
    estimatedDepartureTime: '',
  });
  const [error, setError] = useState('');

  const fetchFlights = () => {
    setLoading(true);
    flightApi.getAll()
      .then(setFlights)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(fetchFlights, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await flightApi.create(form);
      setShowForm(false);
      setForm({ flightNumber: '', origin: '', destination: '', estimatedDepartureTime: '' });
      fetchFlights();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to create flight');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this flight?')) return;
    try {
      await flightApi.delete(id);
      fetchFlights();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to delete flight');
    }
  };

  return (
    <Layout>
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h1>Flights</h1>
          <button className="primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : '+ Register Flight'}
          </button>
        </div>

        {error && (
          <div className="card" style={{ background: '#fff5f5', borderColor: 'var(--danger)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.875rem' }}>
            {error}
            <button style={{ marginLeft: '0.5rem', background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }} onClick={() => setError('')}>×</button>
          </div>
        )}

        {showForm && (
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 className="section-title">Register New Flight</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Flight Number</label>
                  <input
                    required
                    placeholder="e.g. AA1234"
                    value={form.flightNumber}
                    onChange={e => setForm({ ...form, flightNumber: e.target.value })}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Estimated Departure Time</label>
                  <input
                    type="datetime-local"
                    required
                    value={form.estimatedDepartureTime}
                    onChange={e => setForm({ ...form, estimatedDepartureTime: e.target.value })}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Origin</label>
                  <input
                    required
                    placeholder="e.g. JFK"
                    value={form.origin}
                    onChange={e => setForm({ ...form, origin: e.target.value })}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Destination</label>
                  <input
                    required
                    placeholder="e.g. LAX"
                    value={form.destination}
                    onChange={e => setForm({ ...form, destination: e.target.value })}
                  />
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button type="submit" className="primary">Register Flight</button>
                <button type="button" className="secondary" onClick={() => setShowForm(false)}>Cancel</button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading flights...</p>
        ) : flights.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No flights registered yet.</p>
            <button className="primary" style={{ marginTop: '1rem' }} onClick={() => setShowForm(true)}>Register Your First Flight</button>
          </div>
        ) : (
          <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)', color: 'var(--text-secondary)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>ID</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Flight Number</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Origin</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Destination</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem 1rem' }}>Est. Departure</th>
                  <th style={{ textAlign: 'right', padding: '0.75rem 1rem' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {flights.map(f => (
                  <tr key={f.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.75rem 1rem' }}>{f.id}</td>
                    <td style={{ padding: '0.75rem 1rem', fontWeight: 500 }}>{f.flightNumber}</td>
                    <td style={{ padding: '0.75rem 1rem' }}>{f.origin}</td>
                    <td style={{ padding: '0.75rem 1rem' }}>{f.destination}</td>
                    <td style={{ padding: '0.75rem 1rem' }}>{new Date(f.estimatedDepartureTime).toLocaleString()}</td>
                    <td style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>
                      <button className="secondary" style={{ fontSize: '0.75rem' }} onClick={() => handleDelete(f.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}
