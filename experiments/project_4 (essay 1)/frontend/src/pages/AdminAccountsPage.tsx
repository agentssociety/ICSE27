import { useState, useEffect } from 'react';
import { listAccounts, lockAccount, unlockAccount } from '../api/services';
import type { AccountResponse } from '../types';

export default function AdminAccountsPage() {
  const [accounts, setAccounts] = useState<AccountResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [lockReason, setLockReason] = useState<{ [key: number]: string }>({});
  const [actionMsg, setActionMsg] = useState('');

  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listAccounts();
      setAccounts(res.data);
    } catch {
      setError('Failed to load accounts');
    } finally {
      setLoading(false);
    }
  };

  const handleLock = async (accountId: number) => {
    const reason = lockReason[accountId] || 'Suspicious activity';
    try {
      await lockAccount(accountId, reason);
      setActionMsg(`Account ${accountId} locked.`);
      loadAccounts();
    } catch {
      setActionMsg(`Failed to lock account ${accountId}.`);
    }
  };

  const handleUnlock = async (accountId: number) => {
    try {
      await unlockAccount(accountId);
      setActionMsg(`Account ${accountId} unlocked.`);
      loadAccounts();
    } catch {
      setActionMsg(`Failed to unlock account ${accountId}.`);
    }
  };

  if (loading) return <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>Loading accounts...</div>;
  if (error) return <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--danger)' }}>{error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Manage Accounts</h2>
        <button className="secondary" onClick={loadAccounts}>Refresh</button>
      </div>
      {actionMsg && (
        <div style={{ padding: '0.5rem 1rem', marginBottom: '1rem', borderRadius: 'var(--radius-s)', background: 'var(--bg-secondary)', fontSize: '0.875rem' }}>
          {actionMsg}
        </div>
      )}
      <div className="card" style={{ overflowX: 'auto' }}>
        {accounts.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No accounts found.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>ID</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Balance</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Daily Limit</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Withdrawn Today</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Status</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map(acct => (
                <tr key={acct.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem', fontWeight: 600 }}>{acct.id}</td>
                  <td style={{ padding: '0.5rem' }}>${acct.balance.toFixed(2)}</td>
                  <td style={{ padding: '0.5rem' }}>${acct.daily_withdrawal_limit.toFixed(2)}</td>
                  <td style={{ padding: '0.5rem' }}>${acct.withdrawn_today.toFixed(2)}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge" style={{ color: acct.locked_reason ? 'var(--danger)' : 'var(--success)' }}>
                      {acct.locked_reason ? `Locked: ${acct.locked_reason}` : 'Active'}
                    </span>
                  </td>
                  <td style={{ padding: '0.5rem', display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
                    {acct.locked_reason ? (
                      <button className="secondary" onClick={() => handleUnlock(acct.id)} style={{ fontSize: '0.8rem' }}>Unlock</button>
                    ) : (
                      <>
                        <input
                          type="text"
                          placeholder="Lock reason"
                          value={lockReason[acct.id] || ''}
                          onChange={e => setLockReason(prev => ({ ...prev, [acct.id]: e.target.value }))}
                          style={{ width: '120px', fontSize: '0.8rem', padding: '0.3rem 0.5rem' }}
                        />
                        <button className="primary" onClick={() => handleLock(acct.id)} style={{ fontSize: '0.8rem' }}>Lock</button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
