import { useState, useEffect } from 'react';
import { listAuthenticationAttempts, listTransactionLogs } from '../api/services';
import type { AuthenticationAttemptResponse, TransactionLogResponse } from '../types';

export default function AuditLogsPage() {
  const [attempts, setAttempts] = useState<AuthenticationAttemptResponse[]>([]);
  const [logs, setLogs] = useState<TransactionLogResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<'attempts' | 'logs'>('attempts');

  useEffect(() => {
    setLoading(true);
    Promise.all([
      listAuthenticationAttempts().catch(() => ({ data: [] })),
      listTransactionLogs().catch(() => ({ data: [] })),
    ])
      .then(([attemptsRes, logsRes]) => {
        setAttempts(Array.isArray(attemptsRes.data) ? attemptsRes.data : []);
        setLogs(Array.isArray(logsRes.data) ? logsRes.data : []);
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load audit logs. Backend may have stub code.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page"><p>Loading audit logs...</p></div>;

  return (
    <div className="page">
      <h1>Audit Logs</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        Authentication attempts and transaction state changes
      </p>

      {error && <div className="card" style={{ background: '#fff3f0', border: '1px solid var(--danger)', padding: '0.75rem', marginBottom: '1rem', color: 'var(--danger)' }}>{error}</div>}

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <button className={tab === 'attempts' ? 'primary' : 'secondary'} onClick={() => setTab('attempts')}>
          Auth Attempts ({attempts.length})
        </button>
        <button className={tab === 'logs' ? 'primary' : 'secondary'} onClick={() => setTab('logs')}>
          Transaction Logs ({logs.length})
        </button>
      </div>

      {tab === 'attempts' && (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          {attempts.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <p style={{ color: 'var(--text-secondary)' }}>No authentication attempts recorded.</p>
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)' }}>
                  <th style={thStyle}>ID</th>
                  <th style={thStyle}>User</th>
                  <th style={thStyle}>Outcome</th>
                  <th style={thStyle}>Method</th>
                  <th style={thStyle}>IP Address</th>
                  <th style={thStyle}>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map(a => (
                  <tr key={a.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                    <td style={tdStyle}>{a.id}</td>
                    <td style={tdStyle}>{a.user_id}</td>
                    <td style={tdStyle}>
                      <span className="badge" style={{ background: a.outcome === 'success' ? '#e8f5e9' : '#fce4ec', color: a.outcome === 'success' ? '#2e7d32' : '#c62828' }}>
                        {a.outcome}
                      </span>
                    </td>
                    <td style={tdStyle}>{a.method}</td>
                    <td style={tdStyle}>{a.ip_address}</td>
                    <td style={tdStyle}>{new Date(a.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {tab === 'logs' && (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          {logs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <p style={{ color: 'var(--text-secondary)' }}>No transaction logs recorded.</p>
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: 'var(--bg-secondary)' }}>
                  <th style={thStyle}>ID</th>
                  <th style={thStyle}>Log Record</th>
                </tr>
              </thead>
              <tbody>
                {logs.map(l => (
                  <tr key={l.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                    <td style={tdStyle}>{l.id}</td>
                    <td style={tdStyle}>{l.logRecord}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

const thStyle: React.CSSProperties = { textAlign: 'left', padding: '0.75rem 1rem', fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)' };
const tdStyle: React.CSSProperties = { padding: '0.75rem 1rem', fontSize: '0.9rem' };
