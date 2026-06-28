import { useState, useEffect } from 'react';
import { getPatients, assignUrgency } from '../api/services';
import type { Patient, UrgencyLevel } from '../types';

export default function AssignUrgencyPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<number | ''>('');
  const [level, setLevel] = useState<UrgencyLevel>(3);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await getPatients();
        setPatients(data);
      } catch {
        setError('Failed to load patients.');
      } finally {
        setLoading(false);
      }
    };
    fetchPatients();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedPatientId === '') {
      setError('Please select a patient.');
      return;
    }
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      await assignUrgency(selectedPatientId as number, level);
      const patient = patients.find(p => p.id === selectedPatientId);
      setSuccess(`Urgency level ${level} assigned to ${patient?.username || 'patient'}.`);
      setSelectedPatientId('');
      setLevel(3);
    } catch {
      setError('Failed to assign urgency level.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="page">
        <h1>Assign Urgency Level</h1>
        <p style={{ marginTop: '2rem' }}>Loading patients...</p>
      </div>
    );
  }

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Assign Urgency Level</h1>

      {error && (
        <div className="card" style={{ background: '#fff2f0', border: '1px solid #ffccc7', marginBottom: '1rem', padding: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>{error}</p>
        </div>
      )}

      {success && (
        <div className="card" style={{ background: '#f6ffed', border: '1px solid #b7eb8f', marginBottom: '1rem', padding: '1rem' }}>
          <p style={{ color: 'var(--success)' }}>{success}</p>
        </div>
      )}

      <div className="card">
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Select Patient
            </label>
            <select
              value={selectedPatientId}
              onChange={(e) => setSelectedPatientId(e.target.value ? Number(e.target.value) : '')}
              disabled={submitting}
            >
              <option value="">-- Choose a patient --</option>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.username} (ID: {p.id})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Urgency Level
            </label>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {([1, 2, 3, 4, 5] as UrgencyLevel[]).map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  className={level === lvl ? 'primary' : 'secondary'}
                  onClick={() => setLevel(lvl)}
                  style={{ flex: 1, minWidth: '60px', justifyContent: 'center' }}
                  disabled={submitting}
                >
                  {lvl}
                </button>
              ))}
            </div>
            <p style={{ marginTop: '0.375rem', color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>
              {level === 1 && '1 - Non-urgent'}
              {level === 2 && '2 - Low urgency'}
              {level === 3 && '3 - Moderate urgency'}
              {level === 4 && '4 - High urgency'}
              {level === 5 && '5 - Critical'}
            </p>
          </div>

          <button type="submit" className="primary" disabled={submitting || patients.length === 0}>
            {submitting ? 'Assigning...' : 'Assign Urgency Level'}
          </button>
        </form>
      </div>
    </div>
  );
}
