import { useState, useEffect } from 'react';
import { listRunways, createRunway, updateRunway, deleteRunway } from '../api/services';
import type { RunwayResponse, RunwayCreate, RunwayUpdate } from '../types';

export default function RunwaysPage() {
  const [runways, setRunways] = useState<RunwayResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<RunwayCreate>({ runwayId: '', length: undefined });
  const [saving, setSaving] = useState(false);

  const load = () => {
    setLoading(true);
    listRunways()
      .then(data => setRunways(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (editingId !== null) {
        const upd: RunwayUpdate = { runwayId: form.runwayId, length: form.length || undefined };
        await updateRunway(editingId, upd);
      } else {
        await createRunway(form);
      }
      setForm({ runwayId: '', length: undefined });
      setEditingId(null);
      await load();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const startEdit = (r: RunwayResponse) => {
    setEditingId(r.id);
    setForm({ runwayId: r.runwayId, length: r.length });
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this runway?')) return;
    try {
      await deleteRunway(id);
      await load();
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) return <div className="page"><p>Loading runways...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <h1>Runway Management</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Manage runways and handle closures
      </p>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 className="section-title">{editingId ? 'Edit Runway' : 'Add Runway'}</h2>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem', alignItems: 'end', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 200 }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Runway ID</label>
            <input placeholder="e.g. 09L/27R" value={form.runwayId} onChange={e => setForm(p => ({ ...p, runwayId: e.target.value }))} required />
          </div>
          <div style={{ flex: 1, minWidth: 150 }}>
            <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Length (m)</label>
            <input type="number" placeholder="e.g. 3000" value={form.length ?? ''} onChange={e => setForm(p => ({ ...p, length: e.target.value ? parseInt(e.target.value) : undefined }))} />
          </div>
          <button type="submit" className="primary" disabled={saving}>
            {saving ? 'Saving...' : editingId ? 'Update Runway' : 'Add Runway'}
          </button>
          {editingId && (
            <button type="button" className="secondary" onClick={() => { setEditingId(null); setForm({ runwayId: '', length: undefined }); }}>Cancel</button>
          )}
        </form>
      </div>

      <div className="card">
        <h2 className="section-title">All Runways ({runways.length})</h2>
        {runways.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No runways configured yet.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ color: 'var(--text-secondary)', textAlign: 'left' }}>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>ID</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Runway</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Length (m)</th>
                  <th style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {runways.map(r => (
                  <tr key={r.id}>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)', fontWeight: 600 }}>{r.id}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{r.runwayId}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>{r.length}</td>
                    <td style={{ padding: '0.5rem 0.75rem', borderBottom: '1px solid var(--border-light)' }}>
                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem' }} onClick={() => startEdit(r)}>Edit</button>
                        <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.75rem', color: 'var(--danger)' }} onClick={() => handleDelete(r.id)}>Delete</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
