import { useState, useEffect } from 'react';
import { listTransfusionRequests, createTransfusionRequest, deleteTransfusionRequest } from '../api/services';
import type { TransfusionRequest, TransfusionRequestCreate } from '../types';

export default function TransfusionRequestsPage() {
  const [requests, setRequests] = useState<TransfusionRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<TransfusionRequestCreate>({
    requestId: '',
    patientId: '',
    patientABORh: '',
    bloodType: '',
    patientID: ''
  });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    try {
      setLoading(true);
      const data = await listTransfusionRequests();
      setRequests(data);
      setError(null);
    } catch (err) {
      setError('Failed to load transfusion requests.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.requestId || !formData.patientId || !formData.patientABORh || !formData.bloodType || !formData.patientID) return;
    setSubmitting(true);
    try {
      await createTransfusionRequest(formData);
      setFormData({ requestId: '', patientId: '', patientABORh: '', bloodType: '', patientID: '' });
      setShowForm(false);
      await loadRequests();
    } catch (err) {
      setError('Failed to create transfusion request.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteTransfusionRequest(id);
      await loadRequests();
    } catch (err) {
      setError('Failed to delete request.');
    }
  };

  if (loading && requests.length === 0) return <div className="page"><p>Loading transfusion requests...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>Transfusion Request Intake</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'New Request'}
        </button>
      </div>

      {error && <p style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</p>}

      {showForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 className="section-title">Record Transfusion Request</h2>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Request ID</label>
              <input
                type="text"
                value={formData.requestId}
                onChange={e => setFormData({ ...formData, requestId: e.target.value })}
                required
                placeholder="e.g. REQ-001"
              />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Patient ID</label>
              <input
                type="text"
                value={formData.patientId}
                onChange={e => setFormData({ ...formData, patientId: e.target.value })}
                required
                placeholder="e.g. PAT-001"
              />
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Patient ABO/Rh Type</label>
              <select
                value={formData.patientABORh}
                onChange={e => setFormData({ ...formData, patientABORh: e.target.value })}
                required
              >
                <option value="">Select patient type</option>
                <option value="O-">O-</option>
                <option value="O+">O+</option>
                <option value="A-">A-</option>
                <option value="A+">A+</option>
                <option value="B-">B-</option>
                <option value="B+">B+</option>
                <option value="AB-">AB-</option>
                <option value="AB+">AB+</option>
              </select>
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Required Blood Type</label>
              <select
                value={formData.bloodType}
                onChange={e => setFormData({ ...formData, bloodType: e.target.value })}
                required
              >
                <option value="">Select required type</option>
                <option value="O-">O-</option>
                <option value="O+">O+</option>
                <option value="A-">A-</option>
                <option value="A+">A+</option>
                <option value="B-">B-</option>
                <option value="B+">B+</option>
                <option value="AB-">AB-</option>
                <option value="AB+">AB+</option>
              </select>
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Patient ID (duplicate field)</label>
              <input
                type="text"
                value={formData.patientID}
                onChange={e => setFormData({ ...formData, patientID: e.target.value })}
                required
                placeholder="e.g. PAT-001"
              />
              <small style={{ color: 'var(--text-tertiary)' }}>This field is required by the backend schema.</small>
            </div>
            <button className="primary" type="submit" disabled={submitting}>
              {submitting ? 'Saving...' : 'Save Request'}
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="section-title">All Transfusion Requests</h2>
        {requests.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No transfusion requests recorded yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>Request ID</th>
                <th style={{ padding: '0.5rem' }}>Patient ID</th>
                <th style={{ padding: '0.5rem' }}>Patient ABO/Rh</th>
                <th style={{ padding: '0.5rem' }}>Required Blood Type</th>
                <th style={{ padding: '0.5rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(r => (
                <tr key={r.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem' }}>{r.requestId}</td>
                  <td style={{ padding: '0.5rem' }}>{r.patientId}</td>
                  <td style={{ padding: '0.5rem' }}>{r.patientABORh}</td>
                  <td style={{ padding: '0.5rem' }}>{r.bloodType}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <button className="secondary" onClick={() => handleDelete(r.id)}>Delete</button>
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
