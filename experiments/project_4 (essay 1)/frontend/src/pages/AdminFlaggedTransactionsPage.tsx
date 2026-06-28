import { useState, useEffect } from 'react';
import { listFlaggedTransactions, reviewFlaggedTransaction } from '../api/services';
import type { TransactionResponse } from '../types';

export default function AdminFlaggedTransactionsPage() {
  const [flagTxns, setFlagTxns] = useState<TransactionResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionMsg, setActionMsg] = useState('');

  useEffect(() => {
    loadFlagged();
  }, []);

  const loadFlagged = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listFlaggedTransactions();
      setFlagTxns(res.data);
    } catch {
      setError('Failed to load flagged transactions');
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (txnId: string, action: 'approve' | 'reject' | 'escalate') => {
    try {
      await reviewFlaggedTransaction(txnId, action, 'admin');
      setActionMsg(`Transaction ${txnId.slice(0, 8)}... ${action}d successfully.`);
      loadFlagged();
    } catch {
      setActionMsg(`Failed to ${action} transaction.`);
    }
  };

  if (loading) return <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>Loading flagged transactions...</div>;
  if (error) return <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--danger)' }}>{error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2>Flagged Transactions</h2>
        <button className="secondary" onClick={loadFlagged}>Refresh</button>
      </div>
      {actionMsg && (
        <div style={{ padding: '0.5rem 1rem', marginBottom: '1rem', borderRadius: 'var(--radius-s)', background: 'var(--bg-secondary)', fontSize: '0.875rem' }}>
          {actionMsg}
        </div>
      )}
      <div className="card" style={{ overflowX: 'auto' }}>
        {flagTxns.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No flagged transactions found.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Transaction ID</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Timestamp</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Status</th>
                <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {flagTxns.map(txn => (
                <tr key={txn.transaction_id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem', fontFamily: 'monospace', fontSize: '0.8125rem' }}>{txn.transaction_id}</td>
                  <td style={{ padding: '0.5rem', color: 'var(--text-secondary)' }}>{new Date(txn.timestamp).toLocaleString()}</td>
                  <td style={{ padding: '0.5rem' }}>
                    <span className="badge" style={{ color: 'var(--warning)' }}>Flagged</span>
                  </td>
                  <td style={{ padding: '0.5rem', display: 'flex', gap: '0.5rem' }}>
                    <button className="primary" onClick={() => handleAction(txn.transaction_id, 'approve')} style={{ fontSize: '0.8rem', background: 'var(--success)' }}>Approve</button>
                    <button className="secondary" onClick={() => handleAction(txn.transaction_id, 'reject')} style={{ fontSize: '0.8rem', color: 'var(--danger)', borderColor: 'var(--danger)' }}>Reject</button>
                    <button className="secondary" onClick={() => handleAction(txn.transaction_id, 'escalate')} style={{ fontSize: '0.8rem', color: 'var(--warning)' }}>Escalate</button>
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
