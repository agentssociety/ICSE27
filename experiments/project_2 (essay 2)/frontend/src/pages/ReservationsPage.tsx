import { useState, useEffect } from 'react';
import { listReservations, createReservation, deleteReservation } from '../api/services';
import { listBloodUnits, listTransfusionRequests } from '../api/services';
import type { Reservation, ReservationCreate, BloodUnit, TransfusionRequestDTO } from '../types';

export default function ReservationsPage() {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [bloodUnits, setBloodUnits] = useState<BloodUnit[]>([]);
  const [requests, setRequests] = useState<TransfusionRequestDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<ReservationCreate>({
    bloodUnitId: '',
    transfusionRequestId: '',
    bloodUnit_id: 0,
  });

  const fetchData = () => {
    setLoading(true);
    Promise.all([listReservations(), listBloodUnits(), listTransfusionRequests()])
      .then(([res, units, reqs]) => {
        setReservations(res);
        setBloodUnits(units);
        setRequests(reqs);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load data');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const selectedUnit = bloodUnits.find((u) => u.uniqueID === form.bloodUnitId);
      if (!selectedUnit) {
        alert('Please select a valid blood unit');
        return;
      }
      await createReservation({
        ...form,
        bloodUnit_id: selectedUnit.id,
      });
      setShowForm(false);
      setForm({ bloodUnitId: '', transfusionRequestId: '', bloodUnit_id: 0 });
      fetchData();
    } catch (err: any) {
      alert('Failed to create reservation: ' + (err.message || 'Unknown error'));
    }
  };

  const handleRelease = async (id: string) => {
    if (!window.confirm('Release this reservation?')) return;
    try {
      await deleteReservation(id);
      fetchData();
    } catch (err: any) {
      alert('Failed to release reservation: ' + (err.message || 'Unknown error'));
    }
  };

  if (loading) {
    return (
      <div className="page">
        <h1>Reservations</h1>
        <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Loading reservations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <h1>Reservations</h1>
        <div className="card" style={{ borderColor: 'var(--danger)', marginTop: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>Error: {error}</p>
          <button className="primary" style={{ marginTop: '1rem' }} onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Reservations</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Reservation'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginTop: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Create Reservation</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Blood Unit</label>
              <select value={form.bloodUnitId} onChange={(e) => setForm({ ...form, bloodUnitId: e.target.value })}>
                <option value="">Select a unit</option>
                {bloodUnits.filter((u) => u.status === 'available').map((u) => (
                  <option key={u.uniqueID} value={u.uniqueID}>{u.uniqueID} ({u.aboType}{u.rhFactor})</option>
                ))}
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Transfusion Request</label>
              <select value={form.transfusionRequestId} onChange={(e) => setForm({ ...form, transfusionRequestId: e.target.value })}>
                <option value="">Select a request</option>
                {requests.map((r, idx) => (
                  <option key={idx} value={`req-${idx}`}>Request {r.bloodType}{r.rhFactor} - {r.quantity}u</option>
                ))}
              </select>
            </div>
          </div>
          <button type="submit" className="primary" style={{ marginTop: '1rem' }}>Create Reservation</button>
        </form>
      )}

      <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {reservations.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No reservations yet.</p>
        ) : (
          reservations.map((res) => (
            <div key={res.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontWeight: 600 }}>Reservation #{res.id.slice(0, 8)}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                  Unit: {res.bloodUnitId} · Request: {res.transfusionRequestId.slice(0, 8)}
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span className="badge" style={{ background: res.status === 'active' ? 'var(--success)' : 'var(--text-secondary)', color: '#fff' }}>
                  {res.status || 'active'}
                </span>
                <button className="secondary" onClick={() => handleRelease(res.id)}>Release</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
