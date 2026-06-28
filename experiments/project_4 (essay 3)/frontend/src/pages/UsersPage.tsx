import { useState, useEffect } from 'react';
import { listUsers, createUser, deactivateUser, activateUser, deleteUser } from '../api/services';
import type { UserResponse, UserCreateRequest } from '../types';

export default function UsersPage() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [newUser, setNewUser] = useState<UserCreateRequest>({ username: '', email: '', password_hash: '', role: 'user' });

  const fetchUsers = () => {
    setLoading(true);
    setError(null);
    listUsers()
      .then(res => {
        setUsers(res.data?.items ?? []);
        setTotal(res.data?.total ?? 0);
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load users. Backend may have stub code.');
        setUsers([]);
        setTotal(0);
        setLoading(false);
      });
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleCreate = async () => {
    if (!newUser.username || !newUser.email) return;
    try {
      await createUser(newUser);
      setShowCreate(false);
      setNewUser({ username: '', email: '', password_hash: '', role: 'user' });
      fetchUsers();
    } catch {
      setError('Failed to create user (stub backend may reject).');
    }
  };

  const handleToggleStatus = async (user: UserResponse) => {
    try {
      if (user.status === 'active') {
        await deactivateUser(user.id);
      } else {
        await activateUser(user.id);
      }
      fetchUsers();
    } catch {
      setError('Failed to update user status (stub).');
    }
  };

  const handleDelete = async (userId: string) => {
    try {
      await deleteUser(userId);
      fetchUsers();
    } catch {
      setError('Failed to delete user (stub).');
    }
  };

  if (loading) return <div className="page"><p>Loading users...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1>Users</h1>
          <p style={{ color: 'var(--text-secondary)' }}>{total} registered users</p>
        </div>
        <button className="primary" onClick={() => setShowCreate(!showCreate)}>
          {showCreate ? 'Cancel' : '+ New User'}
        </button>
      </div>

      {error && <div className="card" style={{ background: '#fff3f0', border: '1px solid var(--danger)', padding: '0.75rem', marginBottom: '1rem', color: 'var(--danger)' }}>{error}</div>}

      {showCreate && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Create New User</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Username</label>
              <input value={newUser.username} onChange={e => setNewUser({ ...newUser, username: e.target.value })} placeholder="username" />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Email</label>
              <input value={newUser.email} onChange={e => setNewUser({ ...newUser, email: e.target.value })} placeholder="email@example.com" />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Password</label>
              <input type="password" value={newUser.password_hash} onChange={e => setNewUser({ ...newUser, password_hash: e.target.value })} placeholder="password" />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Role</label>
              <select value={newUser.role} onChange={e => setNewUser({ ...newUser, role: e.target.value })}>
                <option value="user">User</option>
                <option value="admin">Admin</option>
                <option value="superadmin">Superadmin</option>
              </select>
            </div>
          </div>
          <div style={{ marginTop: '1rem' }}>
            <button className="primary" onClick={handleCreate}>Create User</button>
          </div>
        </div>
      )}

      {users.length === 0 && !error ? (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No users found. Create one to get started.</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)' }}>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Username</th>
                <th style={thStyle}>Email</th>
                <th style={thStyle}>Role</th>
                <th style={thStyle}>Status</th>
                <th style={thStyle}>Created</th>
                <th style={thStyle}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                  <td style={tdStyle}>{u.id}</td>
                  <td style={tdStyle}>{u.username}</td>
                  <td style={tdStyle}>{u.email}</td>
                  <td style={tdStyle}><span className="badge">{u.role}</span></td>
                  <td style={tdStyle}>
                    <span className="badge" style={{ background: u.status === 'active' ? '#e8f5e9' : '#fce4ec', color: u.status === 'active' ? '#2e7d32' : '#c62828' }}>
                      {u.status}
                    </span>
                  </td>
                  <td style={tdStyle}>{new Date(u.created_at).toLocaleDateString()}</td>
                  <td style={tdStyle}>
                    <div style={{ display: 'flex', gap: '0.3rem' }}>
                      <button
                        className="secondary"
                        style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem' }}
                        onClick={() => handleToggleStatus(u)}
                      >
                        {u.status === 'active' ? 'Deactivate' : 'Activate'}
                      </button>
                      <button
                        style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', background: 'var(--danger)', color: '#fff' }}
                        onClick={() => handleDelete(u.id)}
                      >
                        Delete
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
