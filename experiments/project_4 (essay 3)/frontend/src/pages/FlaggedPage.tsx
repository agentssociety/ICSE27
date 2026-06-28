import { useState, useEffect } from 'react';
import { listFlaggedTransactions, reviewFlaggedTransaction } from '../api/services';
import type { FlaggedTransactionResponse } from '../types';

export default function FlaggedPage() {
  const [flagged, setFlagged] = useState<FlaggedTransactionResponse[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewerId, setReviewerId] = useState('admin-001');

  const fetchFlagged = () => {
    setLoading(true);
    setError(null);
    listFlaggedTransactions()
      .then(res => {
        setFlagged(res.data?.items ?? []);
        setTotal(res.data?.total ?? 0);
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load flagged transactions. Backend may have stub code.');
        setFlagged([]);
        setTotal(0);
        setLoading(false);
      });
  };

  useEffect(() => { fetchFlagged(); }, []);

  const handleReview = async (id: string, action: 'approved' | 'rejected') => {
    try {
      await reviewFlaggedTransaction(id, { reviewer_id: reviewerId });
      fetchFlagged();
    } catch {
      setError('Failed to review transaction (stub).');
    }
  };

  if (loading) return <div className="page"><p>Loading flagged transactions...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1>Flagged Transactions</h1>
          <p style={{ color: 'var(--text-secondary)' }}>{total} transactions flagged for review</p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <label style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Reviewer ID:</label>
          <input value={reviewerId} onChange={e => setReviewerId(e.target.value)} style={{ width: 140 }} />
        </div>
      </div>

      {error && <div className="card" style={{ background: '#fff3f0', border: '1px solid var(--danger)', padding: '0.75rem', marginBottom: '1rem', color: 'var(--danger)' }}>{error}</div>}

      {flagged.length === 0 && !error ? (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No flagged transactions. All clear!</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)' }}>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Withdrawal</th>
                <th style={thStyle}>Reason</th>
                <th style={thStyle}>Flagged At</th>
                <th style={thStyle}>Status</th>
                <th style={thStyle}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {flagged.map(f => (
                <tr key={f.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                  <td style={tdStyle}>{f.id}</td>
                  <td style={tdStyle}>{f.withdrawal_id}</td>
                  <td style={tdStyle}><span style={{ fontSize: '0.85rem' }}>{f.reason}</span></td>
                  <td style={tdStyle}>{new Date(f.flagged_at).toLocaleString()}</td>
                  <td style={tdStyle}><span className="badge">{f.status}</span></td>
                  <td style={tdStyle}>
                    <div style={{ display: 'flex', gap: '0.4rem' }}>
                      <button className="primary" style={{ padding: '0.3rem 0.7rem', fontSize: '0.8rem' }} onClick={() => handleReview(f.id, 'approved')}>
                        Approve
                      </button>
                      <button className="secondary" style={{ padding: '0.3rem 0.7rem', fontSize: '0.8rem' }} onClick={() => handleReview(f.id, 'rejected')}>
                        Reject
                      </button>
                    </div>
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

const thStyle: React.CSSProperties = { textAlign: 'left', padding: '0.75rem 1rem', fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-secondary)' };
const tdStyle: React.CSSProperties = { padding: '0.75rem 1rem', fontSize: '0.9rem' };
