
import { useState, useEffect } from 'react';
import { listBloodUnits, createBloodUnit, deleteBloodUnit } from '../api/services';
import type { BloodUnit, BloodUnitCreate } from '../types';

export default function BloodUnitsPage() {
  const [units, setUnits] = useState<BloodUnit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<BloodUnitCreate>({
    uniqueID: '',
    aboType: 'A',
    rhFactor: '+',
    collectionDate: new Date().toISOString().split('T')[0],
  });

  const fetchUnits = () => {
    setLoading(true);
    listBloodUnits()
      .then((data) => {
        setUnits(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load blood units');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchUnits();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createBloodUnit({
        ...form,
        collectionDate: form.collectionDate,
      });
      setShowForm(false);
      setForm({
        uniqueID: '',
        aboType: 'A',
        rhFactor: '+',
        collectionDate: new Date().toISOString().split('T')[0],
      });
      fetchUnits();
    } catch (err: any) {
      alert('Failed to create blood unit: ' + (err.message || 'Unknown error'));
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this blood unit?')) return;
    try {
      await deleteBloodUnit(id);
      fetchUnits();
    } catch (err: any) {
      alert('Failed to delete blood unit: ' + (err.message || 'Unknown error'));
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'var(--success)';
      case 'issued': return 'var(--accent)';
      case 'expired': return 'var(--danger)';
      default: return 'var(--text-secondary)';
    }
  };

  if (loading) {
    return (
      <div className="page">
        <h1>Blood Units</h1>
        <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Loading blood units...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <h1>Blood Units</h1>
        <div className="card" style={{ borderColor: 'var(--danger)', marginTop: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>Error: {error}</p>
          <button className="primary" style={{ marginTop: '1rem' }} onClick={fetchUnits}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Blood Units</h1>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Blood Unit'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card" style={{ marginTop: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Register New Blood Unit</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Unique ID</label>
              <input required value={form.uniqueID} onChange={(e) => setForm({ ...form, uniqueID: e.target.value })} placeholder="e.g. BLD-0001" />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Collection Date</label>
              <input type="date" required value={form.collectionDate} onChange={(e) => setForm({ ...form, collectionDate: e.target.value })} />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>ABO Type</label>
              <select value={form.aboType} onChange={(e) => setForm({ ...form, aboType: e.target.value })}>
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
          </div>
          <button type="submit" className="primary" style={{ marginTop: '1rem' }}>Register Unit</button>
        </form>
      )}

      <div style={{ marginTop: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {units.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No blood units registered yet.</p>
        ) : (
          units.map((unit) => {
            const now = new Date();
            const expiry = new Date(unit.expiryDate);
            const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
            return (
              <div key={unit.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 600 }}>{unit.uniqueID}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    {unit.aboType}{unit.rhFactor} · Collected: {unit.collectionDate} · Expires: {unit.expiryDate}
                    {daysUntilExpiry <= 7 && daysUntilExpiry >= 0 && (
                      <span style={{ color: 'var(--warning)', marginLeft: '0.5rem' }}>({daysUntilExpiry}d remaining)</span>
                    )}
                    {daysUntilExpiry < 0 && (
                      <span style={{ color: 'var(--danger)', marginLeft: '0.5rem' }}>(Expired)</span>
                    )}
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span className="badge" style={{ background: getStatusColor(unit.status), color: '#fff' }}>
                    {unit.status}
                  </span>
                  <button className="secondary" onClick={() => handleDelete(unit.id)}>Delete</button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
