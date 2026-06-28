import { useState, useEffect } from 'react';
import { getDashboard } from '../api/services';
import type { DashboardItem } from '../types';

export default function DashboardPage() {
  const [items, setItems] = useState<DashboardItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const data = await getDashboard();
      const sorted = data.sort((a, b) => {
        if (a.urgency_level !== b.urgency_level) return a.urgency_level - b.urgency_level;
        return new Date(a.arrival_time).getTime() - new Date(b.arrival_time).getTime();
      });
      setItems(sorted);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch dashboard');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
    const interval = setInterval(fetchDashboard, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

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

  if (loading) return <div className="page"><p>Loading dashboard...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>{error}</p></div>;

  return (
    <div className="page">
      <h1 className="section-title">Live Dashboard</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        Auto-refreshes every 30 seconds. Shows urgency levels and estimated wait times.
      </p>
      {items.length === 0 ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>No patients in the queue.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {items.map((item) => {
            const urg = urgencyLabel(item.urgency_level);
            return (
              <div key={item.patient_id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <p style={{ fontWeight: 600 }}>{item.symptoms}</p>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Arrived: {new Date(item.arrival_time).toLocaleString()}
                  </p>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    Queue position: {item.queue_position}
                  </p>
                </div>
                <span className="badge" style={{ background: urg.color, color: '#fff' }}>
                  {urg.label} ({item.urgency_level})
                </span>
                <div style={{ textAlign: 'right' }}>
                  <p style={{ fontWeight: 600, color: 'var(--accent)' }}>
                    {item.estimated_wait_minutes} min
                  </p>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>est. wait</p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
