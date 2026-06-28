import { useState, useEffect } from 'react';
import { listAccounts, createAccount } from '../api/services';
import type { AccountResponse, AccountCreateRequest } from '../types';

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<AccountResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [newAccount, setNewAccount] = useState<AccountCreateRequest>({ account_id: '' });

  const fetchAccounts = () => {
    setLoading(true);
    setError(null);
    listAccounts()
      .then(res => { setAccounts(Array.isArray(res.data) ? res.data : []); setLoading(false); })
      .catch(err => {
        setError('Could not load accounts. Backend may have stub code.');
        setAccounts([]);
        setLoading(false);
      });
  };

  useEffect(() => { fetchAccounts(); }, []);

  const handleCreate = async () => {
    if (!newAccount.account_id) return;
    try {
      await createAccount(newAccount);
      setShowCreate(false);
      setNewAccount({ account_id: '' });
      fetchAccounts();
    } catch {
      setError('Failed to create account (stub backend may reject).');
    }
  };

  if (loading) return <div className="page"><p>Loading accounts...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1>Accounts</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Manage bank accounts</p>
        </div>
        <button className="primary" onClick={() => setShowCreate(!showCreate)}>
          {showCreate ? 'Cancel' : '+ New Account'}
        </button>
      </div>

      {error && <div className="card" style={{ background: '#fff3f0', border: '1px solid var(--danger)', padding: '0.75rem', marginBottom: '1rem', color: 'var(--danger)' }}>{error}</div>}

      {showCreate && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Create New Account</h3>
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Account ID</label>
              <input value={newAccount.account_id} onChange={e => setNewAccount({ ...newAccount, account_id: e.target.value })} placeholder="e.g., ACCT-1001" />
            </div>
            <button className="primary" onClick={handleCreate}>Create</button>
          </div>
        </div>
      )}

      {accounts.length === 0 && !error ? (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No accounts found. Create one to get started.</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)' }}>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Account ID</th>
                <th style={thStyle}>Balance</th>
                <th style={thStyle}>Locked</th>
                <th style={thStyle}>Failed Attempts</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map(acc => (
                <tr key={acc.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                  <td style={tdStyle}>{acc.id}</td>
                  <td style={tdStyle}>{acc.account_id}</td>
                  <td style={tdStyle}>${acc.balance?.toFixed(2) ?? 'N/A'}</td>
                  <td style={tdStyle}>{acc.locked ? '🔒 Yes' : '🔓 No'}</td>
                  <td style={tdStyle}>{acc.failed_attempt_count}</td>
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
