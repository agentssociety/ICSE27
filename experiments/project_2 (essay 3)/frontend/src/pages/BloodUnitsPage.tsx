import { useState, useEffect } from 'react';
import { listBloodUnits, createBloodUnit, deleteBloodUnit } from '../api/services';
import type { BloodUnit, BloodUnitCreate } from '../types';

export default function BloodUnitsPage() {
  const [units, setUnits] = useState<BloodUnit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<BloodUnitCreate>({ abo_rh_type: '', collection_date: '' });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadUnits();
  }, []);

  const loadUnits = async () => {
    try {
      setLoading(true);
      const data = await listBloodUnits();
      setUnits(data);
      setError(null);
    } catch (err) {
      setError('Failed to load blood units.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.abo_rh_type || !formData.collection_date) return;
    setSubmitting(true);
    try {
      await createBloodUnit(formData);
      setFormData({ abo_rh_type: '', collection_date: '' });
      setShowForm(false);
      await loadUnits();
    } catch (err) {
      setError('Failed to create blood unit.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteBloodUnit(id);
      await loadUnits();
    } catch (err) {
      setError('Failed to delete blood unit.');
    }
  };

  if (loading && units.length === 0) return <div className="page"><p>Loading blood units...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>Blood Unit Tracking</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add Blood Unit'}
        </button>
      </div>

      {error && <p style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</p>}

      {showForm && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 className="section-title">Record New Blood Unit</h2>
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>ABO/Rh Type</label>
              <select
                value={formData.abo_rh_type}
                onChange={e => setFormData({ ...formData, abo_rh_type: e.target.value })}
                required
              >
                <option value="">Select type</option>
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
              <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Collection Date</label>
              <input
                type="date"
                value={formData.collection_date}
                onChange={e => setFormData({ ...formData, collection_date: e.target.value })}
                required
              />
            </div>
            <button className="primary" type="submit" disabled={submitting}>
              {submitting ? 'Saving...' : 'Save Blood Unit'}
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="section-title">All Blood Units</h2>
        {units.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No blood units recorded yet.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>ID</th>
                <th style={{ padding: '0.5rem' }}>ABO/Rh</th>
                <th style={{ padding: '0.5rem' }}>Collection Date</th>
                <th style={{ padding: '0.5rem' }}>Status</th>
                <th style={{ padding: '0.5rem' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {units.map(u => (
                <tr key={u.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem' }}>{u.id}</td>
                  <td style={{ padding: '0.5rem' }}>{u.abo_rh_type}</td>
                  <td style={{ padding: '0.5rem' }}>{u.collection_date}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge" style={{
                      background: u.is_expired ? 'var(--danger)' : 'var(--success)',
                      color: '#fff'
                    }}>
                      {u.is_expired ? 'Expired' : 'Available'}
                    </span>
                  </td>
                  <td style={{ padding: '0.5rem' }}>
                    <button className="secondary" onClick={() => handleDelete(u.id)}>Delete</button>
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
