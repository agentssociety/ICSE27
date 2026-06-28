import { useState, useEffect } from 'react';
import { listTransfusionRequests, submitTransfusionRequest } from '../api/services';
import type { TransfusionRequestDTO, SubmitResponse } from '../types';

export default function TransfusionRequestsPage() {
  const [requests, setRequests] = useState<TransfusionRequestDTO[]>([]);
  const [submitResult, setSubmitResult] = useState<SubmitResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<TransfusionRequestDTO>({
    bloodType: 'A',
    rhFactor: '+',
    quantity: 1,
  });
  const [submitting, setSubmitting] = useState(false);

  const fetchRequests = () => {
    setLoading(true);
    listTransfusionRequests()
      .then((data) => {
        setRequests(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load requests');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const result = await submitTransfusionRequest(form);
      setSubmitResult(result);
      setShowForm(false);
      setForm({ bloodType: 'A', rhFactor: '+', quantity: 1 });
      fetchRequests();
    } catch (err: any) {
      alert('Failed to submit request: ' + (err.message || 'Unknown error'));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <h1>Transfusion Requests</h1>
        <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Loading requests...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <h1>Transfusion Requests</h1>
        <div className="card" style={{ borderColor: 'var(--danger)', marginTop: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>Error: {error}</p>
          <button className="primary" style={{ marginTop: '1rem' }} onClick={fetchRequests}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Transfusion Requests</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Request'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginTop: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Submit Transfusion Request</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Blood Type</label>
              <select value={form.bloodType} onChange={(e) => setForm({ ...form, bloodType: e.target.value })}>
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="AB">AB</option>
                <option value="O">O</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Rh Factor</label>
              <select value={form.rhFactor} onChange={(e) => setForm({ ...form, rhFactor: e.target.value })}>
                <option value="+">+</option>
                <option value="-">-</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Quantity</label>
              <input type="number" min={1} required value={form.quantity} onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value) || 1 })} />
            </div>
          </div>
          <button type="submit" className="primary" style={{ marginTop: '1rem' }} disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit Request'}
          </button>
        </form>
      )}

      {submitResult && (
        <div className="card" style={{ marginTop: '1rem', borderColor: submitResult.success ? 'var(--success)' : 'var(--danger)' }}>
          <p style={{ color: submitResult.success ? 'var(--success)' : 'var(--danger)' }}>
            {submitResult.message} (ID: {submitResult.requestId.slice(0, 8)})
          </p>
        </div>
      )}

      <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {requests.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No transfusion requests yet.</p>
        ) : (
          requests.map((req, idx) => (
            <div key={idx} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontWeight: 600 }}>{req.bloodType}{req.rhFactor} - {req.quantity} unit(s)</div>
              <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>Pending</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
