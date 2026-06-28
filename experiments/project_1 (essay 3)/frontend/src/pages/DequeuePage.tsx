import { useState } from 'react';
import { dequeueNext } from '../api/services';
import type { QueueItem } from '../types';

export default function DequeuePage() {
  const [nextPatient, setNextPatient] = useState<QueueItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dequeued, setDequeued] = useState(false);

  const handleDequeue = async () => {
    setLoading(true);
    setError(null);
    setDequeued(false);
    setNextPatient(null);

    try {
      const patient = await dequeueNext();
      if (patient) {
        setNextPatient(patient);
        setDequeued(true);
      } else {
        setError('No patients in the queue.');
      }
    } catch {
      setError('Failed to dequeue patient. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Take Next Patient</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {error && (
          <div className="card" style={{ background: '#fff2f0', border: '1px solid #ffccc7', padding: '1rem' }}>
            <p style={{ color: 'var(--danger)' }}>{error}</p>
          </div>
        )}

        <button
          className="primary"
          onClick={handleDequeue}
          disabled={loading}
          style={{ alignSelf: 'flex-start', padding: '0.75rem 2rem', fontSize: '1.0625rem' }}
        >
          {loading ? 'Fetching...' : 'Take Next Patient'}
        </button>

        {dequeued && nextPatient && (
          <div className="card">
            <h2 className="section-title">Current Patient</h2>
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              <div>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Name</span>
                <p style={{ fontWeight: 600, fontSize: '1.125rem' }}>{nextPatient.patient.username}</p>
              </div>
              <div>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Patient ID</span>
                <p>{nextPatient.patient.id}</p>
              </div>
              <div>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Urgency Level</span>
                <p>
                  <span
                    className="badge"
                    style={{
                      background: nextPatient.urgency >= 4 ? 'var(--danger)' : nextPatient.urgency >= 3 ? 'var(--warning)' : 'var(--bg-secondary)',
                      color: nextPatient.urgency >= 4 ? '#fff' : 'var(--text)',
                    }}
                  >
                    {nextPatient.urgency}
                  </span>
                </p>
              </div>
              {nextPatient.symptom && (
                <div>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Reported Symptoms</span>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{nextPatient.symptom.description}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {!dequeued && !error && (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>
              Click the button above to dequeue the next patient from the queue.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
