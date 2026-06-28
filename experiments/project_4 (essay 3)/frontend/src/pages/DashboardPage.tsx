import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listAccounts, listWithdrawals, listFlaggedTransactions } from '../api/services';

export default function DashboardPage() {
  const [stats, setStats] = useState({ accounts: 0, withdrawals: 0, flagged: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      listAccounts().catch(() => ({ data: [] })),
      listWithdrawals().catch(() => ({ data: { items: [], total: 0 } })),
      listFlaggedTransactions().catch(() => ({ data: { items: [], total: 0 } })),
    ])
      .then(([accountsRes, withdrawalsRes, flaggedRes]) => {
        setStats({
          accounts: Array.isArray(accountsRes.data) ? accountsRes.data.length : 0,
          withdrawals: withdrawalsRes.data?.total ?? 0,
          flagged: flaggedRes.data?.total ?? 0,
        });
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load dashboard data.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="page"><p>Loading dashboard...</p></div>;

  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Overview of ATM system activity
      </p>

      {error && (
        <div className="card" style={{ background: 'var(--danger)', color: '#fff', marginBottom: '1rem' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '2.5rem', color: 'var(--accent)', margin: '0.5rem 0' }}>{stats.accounts}</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Accounts</p>
          <Link to="/accounts" style={{ fontSize: '0.85rem' }}>View all →</Link>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '2.5rem', color: 'var(--accent)', margin: '0.5rem 0' }}>{stats.withdrawals}</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Withdrawals</p>
          <Link to="/withdrawals" style={{ fontSize: '0.85rem' }}>View all →</Link>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '2.5rem', color: 'var(--accent)', margin: '0.5rem 0' }}>{stats.flagged}</h2>
          <p style={{ color: 'var(--text-secondary)' }}>Flagged Transactions</p>
          <Link to="/flagged" style={{ fontSize: '0.85rem' }}>View all →</Link>
        </div>
      </div>
    </div>
  );
}
