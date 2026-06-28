import { useState, useEffect } from 'react';
import { listWithdrawals, createWithdrawal } from '../api/services';
import type { WithdrawalResponse, WithdrawalCreateRequest } from '../types';

export default function WithdrawalsPage() {
  const [withdrawals, setWithdrawals] = useState<WithdrawalResponse[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newWithdrawal, setNewWithdrawal] = useState<WithdrawalCreateRequest>({ account_id: '', amount: 0 });

  const fetchWithdrawals = () => {
    setLoading(true);
    setError(null);
    listWithdrawals()
      .then(res => {
        setWithdrawals(res.data?.items ?? []);
        setTotal(res.data?.total ?? 0);
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load withdrawals. Backend may have stub code.');
        setWithdrawals([]);
        setTotal(0);
        setLoading(false);
      });
  };

  useEffect(() => { fetchWithdrawals(); }, []);

  const handleCreate = async () => {
    if (!newWithdrawal.account_id || newWithdrawal.amount <= 0) return;
    try {
      await createWithdrawal(newWithdrawal);
      setNewWithdrawal({ account_id: '', amount: 0 });
      fetchWithdrawals();
    } catch {
      setError('Failed to create withdrawal (stub backend may reject).');
    }
  };

  if (loading) return <div className="page"><p>Loading withdrawals...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1>Withdrawals</h1>
          <p style={{ color: 'var(--text-secondary)' }}>{total} total withdrawal transactions</p>
        </div>
      </div>

      {error && <div className="card" style={{ background: '#fff3f0', border: '1px solid var(--danger)', padding: '0.75rem', marginBottom: '1rem', color: 'var(--danger)' }}>{error}</div>}

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>New Withdrawal</h3>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 200 }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Account ID</label>
            <input value={newWithdrawal.account_id} onChange={e => setNewWithdrawal({ ...newWithdrawal, account_id: e.target.value })} placeholder="e.g., ACCT-1001" />
          </div>
          <div style={{ flex: 1, minWidth: 150 }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Amount ($)</label>
            <input type="number" value={newWithdrawal.amount || ''} onChange={e => setNewWithdrawal({ ...newWithdrawal, amount: parseFloat(e.target.value) || 0 })} placeholder="0.00" />
          </div>
          <button className="primary" onClick={handleCreate}>Submit Withdrawal</button>
        </div>
      </div>

      {withdrawals.length === 0 && !error ? (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No withdrawals recorded yet.</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)' }}>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Account</th>
                <th style={thStyle}>Amount</th>
                <th style={thStyle}>Status</th>
                <th style={thStyle}>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {withdrawals.map(w => (
                <tr key={w.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                  <td style={tdStyle}>{w.id}</td>
                  <td style={tdStyle}>{w.account_id}</td>
                  <td style={tdStyle}>${Number(w.amount).toFixed(2)}</td>
                  <td style={tdStyle}><span className="badge">{w.status}</span></td>
                  <td style={tdStyle}>{new Date(w.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const thStyle: React.CSSProperties = { textAlign: 'left', padding: '0.75rem 1rem', fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)' };
const tdStyle: React.CSSProperties = { padding: '0.75rem 1rem', fontSize: '0.9rem' };
