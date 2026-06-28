import { useState, useEffect } from 'react';
import { listPatients, updatePatient, deletePatient } from '../api/services';
import type { PatientResponse } from '../types';

export default function QueuePage() {
  const [patients, setPatients] = useState<PatientResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const data = await listPatients();
      // Sort by urgencyLevel asc, then by arrivalTime asc
      const sorted = data.sort((a, b) => {
        if (a.urgencyLevel !== b.urgencyLevel) return a.urgencyLevel - b.urgencyLevel;
        return new Date(a.arrivalTime).getTime() - new Date(b.arrivalTime).getTime();
      });
      setPatients(sorted);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch queue');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleReTriage = async (patient: PatientResponse) => {
    const newLevel = prompt(`Enter new urgency level (1-5) for ${patient.symptoms}:`, String(patient.urgencyLevel));
    if (!newLevel) return;
    const level = parseInt(newLevel, 10);
    if (isNaN(level) || level < 1 || level > 5) {
      alert('Please enter a valid urgency level between 1 and 5.');
      return;
    }
    const levelMap: Record<number, string> = { 1: 'critical', 2: 'urgent', 3: 'moderate', 4: 'non-urgent', 5: 'minimal' };
    try {
      await updatePatient(patient.id, { urgencyLevel: level, urgency: levelMap[level] || 'moderate' });
      await fetchPatients();
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to update urgency');
    }
  };

  const handleTakePatient = async (patient: PatientResponse) => {
    if (!confirm(`Take patient "${patient.symptoms}" from queue?`)) return;
    try {
      await deletePatient(patient.id);
      await fetchPatients();
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to take patient');
    }
  };

  const urgencyLabel = (level: number) => {
    const map: Record<number, { label: string; color: string }> = {
      1: { label: 'Critical', color: 'var(--danger)' },
      2: { label: 'Urgent', color: 'var(--warning)' },
      3: { label: 'Moderate', color: 'var(--accent)' },
      4: { label: 'Non-urgent', color: 'var(--text-secondary)' },
      5: { label: 'Minimal', color: 'var(--text-tertiary)' },
    };
    return map[level] || { label: 'Unknown', color: 'var(--text-secondary)' };
  };

  if (loading) return <div className="page"><p>Loading queue...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>{error}</p></div>;

  return (
    <div className="page">
      <h1 className="section-title">Patient Queue</h1>
      <div style={{ marginBottom: '1rem' }}>
        <button className="secondary" onClick={fetchPatients}>Refresh Queue</button>
      </div>
      {patients.length === 0 ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>No patients in queue.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {patients.map((patient) => {
            const urg = urgencyLabel(patient.urgencyLevel);
            return (
              <div key={patient.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <p style={{ fontWeight: 600 }}>{patient.symptoms}</p>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Arrived: {new Date(patient.arrivalTime).toLocaleString()}
                  </p>
                </div>
                <span className="badge" style={{ background: urg.color, color: '#fff' }}>
                  {urg.label} ({patient.urgencyLevel})
                </span>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="secondary" onClick={() => handleReTriage(patient)}>Re-triage</button>
                  <button className="primary" onClick={() => handleTakePatient(patient)}>Take Patient</button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
