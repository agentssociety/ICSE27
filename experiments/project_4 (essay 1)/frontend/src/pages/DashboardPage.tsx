import { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import type { UserResponse, AccountResponse, TransactionResponse, AuditLogEntryResponse } from '../types';
import { getTransactionsByUser, listAccounts, listTransactions, createTransaction, listAuditLogs } from '../api/services';

export default function DashboardPage() {
  const location = useLocation();
  const user = (location.state as any)?.user as UserResponse | undefined;
  const account = (location.state as any)?.account as AccountResponse | undefined;

  const [transactions, setTransactions] = useState<TransactionResponse[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogEntryResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [withdrawAmount, setWithdrawAmount] = useState('');
  const [withdrawResult, setWithdrawResult] = useState('');

  useEffect(() => {
    if (!user) return;
    const loadData = async () => {
      try {
        const [txnsRes, auditRes] = await Promise.all([
          getTransactionsByUser(user.userID).catch(() => listTransactions().then(r => ({ data: r.data }))),
          listAuditLogs().catch(() => ({ data: [] })),
        ]);
        setTransactions(Array.isArray(txnsRes.data) ? txnsRes.data : []);
        setAuditLogs(Array.isArray((auditRes as any).data) ? (auditRes as any).data : []);
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [user]);

  const handleWithdraw = async (e: React.FormEvent) => {
    e.preventDefault();
    setWithdrawResult('');
    try {
      const amount = parseFloat(withdrawAmount);
      if (isNaN(amount) || amount <= 0) {
        setWithdrawResult('Please enter a valid amount');
        return;
      }
      // Create a transaction (simulated withdrawal)
      const txn = await createTransaction({
        amount_id: 1, // simplified
        status_id: 1,
        timestamp: new Date().toISOString(),
      });
      setWithdrawResult(`Withdrawal of $${amount.toFixed(2)} initiated successfully (ID: ${txn.data.transaction_id})`);
      setWithdrawAmount('');
      // Reload transactions
      const txnsRes = await getTransactionsByUser(user!.userID);
      setTransactions(Array.isArray(txnsRes.data) ? txnsRes.data : []);
    } catch {
      setWithdrawResult('Withdrawal failed. Please try again.');
    }
  };

  if (!user) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h2>Not Logged In</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>Please log in first.</p>
        <Link to="/login"><button className="primary" style={{ marginTop: '1rem' }}>Go to Login</button></Link>
      </div>
    );
  }

  if (loading) return <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>Loading dashboard...</div>;
  if (error) return <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--danger)' }}>{error}</div>;

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>Welcome, {user.userID}</h2>
      
      {/* Account Info Card */}
      {account && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 className="section-title">Account Summary</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
            <div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Balance</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>${account.balance.toFixed(2)}</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Daily Limit</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>${account.daily_withdrawal_limit.toFixed(2)}</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Withdrawn Today</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>${account.withdrawn_today.toFixed(2)}</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Status</div>
              <div style={{ fontSize: '1rem', fontWeight: 500, color: account.locked_reason ? 'var(--danger)' : 'var(--success)' }}>
                {account.locked_reason ? `Locked: ${account.locked_reason}` : 'Active'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Withdrawal Form */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 className="section-title">Make a Withdrawal</h3>
        <form onSubmit={handleWithdraw} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '0.375rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Amount ($)</label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={withdrawAmount}
              onChange={e => setWithdrawAmount(e.target.value)}
              placeholder="0.00"
              required
            />
          </div>
          <button type="submit" className="primary">Withdraw</button>
        </form>
        {withdrawResult && (
          <div style={{ marginTop: '0.75rem', padding: '0.5rem', borderRadius: 'var(--radius-s)', background: 'var(--bg-secondary)', fontSize: '0.875rem' }}>
            {withdrawResult}
          </div>
        )}
      </div>

      {/* Recent Transactions */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 className="section-title">Recent Transactions</h3>
        {transactions.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No transactions found.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>ID</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Timestamp</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {transactions.slice(0, 10).map(txn => (
                <tr key={txn.transaction_id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem', fontFamily: 'monospace', fontSize: '0.8125rem' }}>{txn.transaction_id.slice(0, 8)}...</td>
                  <td style={{ padding: '0.5rem', color: 'var(--text-secondary)' }}>{new Date(txn.timestamp).toLocaleString()}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge">{txn.status_id === 1 ? 'Pending' : txn.status_id === 2 ? 'Approved' : 'Completed'}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Recent Audit Logs */}
      {auditLogs.length > 0 && (
        <div className="card">
          <h3 className="section-title">Recent Security Events</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Time</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Operation</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Outcome</th>
              </tr>
            </thead>
            <tbody>
              {auditLogs.slice(-5).reverse().map((log, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>{new Date(log.timestamp).toLocaleString()}</td>
                  <td style={{ padding: '0.5rem' }}>{log.operation}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge" style={{ color: log.outcome === 'success' ? 'var(--success)' : 'var(--danger)' }}>{log.outcome}</span>
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
