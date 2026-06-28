import { useState, useEffect } from 'react';
import { getQueue, assignUrgency } from '../api/services';
import type { QueueItem, UrgencyLevel } from '../types';

export default function DashboardPage() {
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQueue = async () => {
    try {
      setLoading(true);
      const data = await getQueue();
      setQueue(data);
      setError(null);
    } catch (err) {
      setError('Failed to load queue. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
    // Refresh every 10 seconds
    const interval = setInterval(fetchQueue, 10000);
    return () => clearInterval(interval);
  }, []);

  const urgencyColor = (level: UrgencyLevel): string => {
    switch (level) {
      case 5: return 'var(--danger)';
      case 4: return 'var(--warning)';
      case 3: return '#ff9500';
      case 2: return '#34c759';
      default: return 'var(--text-secondary)';
    }
  };

  const urgencyLabel = (level: UrgencyLevel): string => {
    switch (level) {
      case 5: return 'Critical';
      case 4: return 'High';
      case 3: return 'Moderate';
      case 2: return 'Low';
      default: return 'Non-urgent';
    }
  };

  if (loading && queue.length === 0) {
    return (
      <div className="page">
        <h1>Live Queue Dashboard</h1>
        <p style={{ marginTop: '2rem' }}>Loading queue data...</p>
      </div>
    );
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>Live Queue Dashboard</h1>
        <button className="secondary" onClick={fetchQueue} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div className="card" style={{ background: '#fff2f0', border: '1px solid #ffccc7', marginBottom: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>{error}</p>
        </div>
      )}

      {queue.length === 0 && !loading ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '2rem' }}>
            No patients in the queue. Everything is up to date.
          </p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.875rem 1rem', textAlign: 'left', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>#</th>
                <th style={{ padding: '0.875rem 1rem', textAlign: 'left', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Patient</th>
                <th style={{ padding: '0.875rem 1rem', textAlign: 'left', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Urgency</th>
                <th style={{ padding: '0.875rem 1rem', textAlign: 'left', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Est. Wait</th>
              </tr>
            </thead>
            <tbody>
              {queue.map((item) => (
                <tr key={item.patient.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.875rem 1rem', color: 'var(--text-secondary)' }}>{item.position}</td>
                  <td style={{ padding: '0.875rem 1rem', fontWeight: 500 }}>{item.patient.username}</td>
                  <td style={{ padding: '0.875rem 1rem' }}>
                    <span
                      className="badge"
                      style={{
                        background: urgencyColor(item.urgency),
                        color: item.urgency >= 4 ? '#fff' : 'var(--text)',
                      }}
                    >
                      {item.urgency} - {urgencyLabel(item.urgency)}
                    </span>
                  </td>
                  <td style={{ padding: '0.875rem 1rem', color: 'var(--text-secondary)' }}>
                    ~{item.estimatedWaitTimeMinutes} min
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
