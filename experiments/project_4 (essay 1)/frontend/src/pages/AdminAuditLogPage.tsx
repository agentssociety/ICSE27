import { useState, useEffect } from 'react';
import { listAuditLogs } from '../api/services';
import type { AuditLogEntryResponse } from '../types';

export default function AdminAuditLogPage() {
  const [auditLogs, setAuditLogs] = useState<AuditLogEntryResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadAuditLogs();
  }, []);

  const loadAuditLogs = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listAuditLogs();
      setAuditLogs(Array.isArray(res.data) ? res.data : []);
    } catch {
      setError('Failed to load audit logs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>Loading audit logs...</div>;
  if (error) return <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--danger)' }}>{error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Audit Log</h2>
        <button className="secondary" onClick={loadAuditLogs}>Refresh</button>
      </div>
      <div className="card" style={{ overflowX: 'auto' }}>
        {auditLogs.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No audit log entries found.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Timestamp</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Username</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Operation</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>IP Address</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Outcome</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Action Type</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.slice().reverse().map((log, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem', fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>{new Date(log.timestamp).toLocaleString()}</td>
                  <td style={{ padding: '0.5rem', fontWeight: 500 }}>{log.username}</td>
                  <td style={{ padding: '0.5rem' }}>{log.operation}</td>
                  <td style={{ padding: '0.5rem', fontFamily: 'monospace', fontSize: '0.8125rem' }}>{log.ip_address}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge" style={{ color: log.outcome === 'success' ? 'var(--success)' : 'var(--danger)' }}>
                      {log.outcome}
                    </span>
                  </td>
                  <td style={{ padding: '0.5rem' }}>{log.action_type || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
