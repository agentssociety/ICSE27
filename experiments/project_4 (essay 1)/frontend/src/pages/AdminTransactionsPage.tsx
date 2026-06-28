import { useState, useEffect } from 'react';
import { listTransactions, listUsers, getTransactionsByUser } from '../api/services';
import type { TransactionResponse, UserResponse } from '../types';

export default function AdminTransactionsPage() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [transactions, setTransactions] = useState<TransactionResponse[]>([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const res = await listUsers();
      setUsers(res.data);
    } catch {
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const loadUserTransactions = async (userId: string) => {
    setLoading(true);
    setError('');
    try {
      const res = await getTransactionsByUser(userId);
      setTransactions(res.data);
    } catch {
      setError('Failed to load transactions for this user');
    } finally {
      setLoading(false);
    }
  };

  const handleUserChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const userId = e.target.value;
    setSelectedUser(userId);
    if (userId) {
      loadUserTransactions(userId);
    } else {
      setTransactions([]);
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>Transaction History</h2>
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Select User</label>
        <select value={selectedUser} onChange={handleUserChange} style={{ maxWidth: '400px' }}>
          <option value="">-- Choose a user --</option>
          {users.map(u => (
            <option key={u.userID} value={u.userID}>{u.userID} (Card: {u.card_id})</option>
          ))}
        </select>
      </div>
      {loading && <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>Loading...</div>}
      {error && <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--danger)' }}>{error}</div>}
      {selectedUser && !loading && !error && (
        <div className="card" style={{ overflowX: 'auto' }}>
          <h3 className="section-title">Transactions for {selectedUser}</h3>
          {transactions.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No transactions found for this user.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)', textAlign: 'left' }}>
                  <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>ID</th>
                  <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Amount ID</th>
                  <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Timestamp</th>
                  <th style={{ padding: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Status ID</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map(txn => (
                  <tr key={txn.transaction_id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.5rem', fontFamily: 'monospace', fontSize: '0.8125rem' }}>{txn.transaction_id}</td>
                    <td style={{ padding: '0.5rem' }}>{txn.amount_id ?? '-'}</td>
                    <td style={{ padding: '0.5rem', color: 'var(--text-secondary)' }}>{new Date(txn.timestamp).toLocaleString()}</td>
                    <td style={{ padding: '0.5rem' }}>{txn.status_id ?? '-'}</td>
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
