import { useState, useEffect } from 'react';
import { listReservations, createReservation, deleteReservation } from '../api/services';
import type { Reservation, ReservationCreate } from '../types';

export default function ReservationsPage() {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<ReservationCreate>({ request_id: 0, unit_id: 0 });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadReservations();
  }, []);

  const loadReservations = async () => {
    try {
      setLoading(true);
      const data = await listReservations();
      setReservations(data);
      setError(null);
    } catch (err) {
      setError('Failed to load reservations.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.request_id || !formData.unit_id) return;
    setSubmitting(true);
    try {
      await createReservation(formData);
      setFormData({ request_id: 0, unit_id: 0 });
      setShowForm(false);
      await loadReservations();
    } catch (err) {
      setError('Failed to create reservation.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteReservation(id);
      await loadReservations();
    } catch (err) {
      setError('Failed to delete reservation.');
    }
  };

  if (loading && reservations.length === 0) return <div className="page"><p>Loading reservations...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>Reservation System</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Create Reservation'}
        </button>
      </div>

      {error && <p style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</p>}

      {showForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 className="section-title">New Reservation</h2>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Request ID</label>
              <input
                type="number"
                value={formData.request_id || ''}
                onChange={e => setFormData({ ...formData, request_id: parseInt(e.target.value) || 0 })}
                required
                placeholder="Enter request ID"
              />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Blood Unit ID</label>
              <input
                type="number"
                value={formData.unit_id || ''}
                onChange={e => setFormData({ ...formData, unit_id: parseInt(e.target.value) || 0 })}
                required
                placeholder="Enter unit ID"
              />
            </div>
            <button className="primary" type="submit" disabled={submitting}>
              {submitting ? 'Saving...' : 'Create Reservation'}
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="section-title">All Reservations</h2>
        {reservations.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No reservations recorded yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>Reservation ID</th>
                <th style={{ padding: '0.5rem' }}>Request ID</th>
                <th style={{ padding: '0.5rem' }}>Unit ID</th>
                <th style={{ padding: '0.5rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reservations.map(r => (
                <tr key={r.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem' }}>{r.id}</td>
                  <td style={{ padding: '0.5rem' }}>{r.request_id ?? '-'}</td>
                  <td style={{ padding: '0.5rem' }}>{r.unit_id ?? '-'}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <button className="secondary" onClick={() => handleDelete(r.id)}>Release</button>
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
