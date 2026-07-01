
import { useState, useEffect } from 'react';
import { listUsers, listAuditLogs, listUserProfiles, updateUserProfile, deleteUser, createAuditLog } from '../api/services';
import type { UserResponse, AuditLogResponse, UserProfileResponse } from '../types';

export default function AdminPage() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogResponse[]>([]);
  const [userProfiles, setUserProfiles] = useState<UserProfileResponse[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    Promise.all([listUsers(), listAuditLogs(), listUserProfiles()])
      .then(([u, a, p]) => {
        setUsers(u);
        setAuditLogs(a);
        setUserProfiles(p);
        if (u.length > 0) setSelectedUserId(u[0].id);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleGrantBadge = async () => {
    if (!selectedUserId) return;
    try {
      await updateUserProfile(selectedUserId, { verifiedBadgeStatus: true });
      setMessage('Verified badge granted');
    } catch { setMessage('Failed to grant badge'); }
  };

  const handleRevokeBadge = async () => {
    if (!selectedUserId) return;
    try {
      await updateUserProfile(selectedUserId, { verifiedBadgeStatus: false });
      setMessage('Verified badge revoked');
    } catch { setMessage('Failed to revoke badge'); }
  };

  const handleDeleteUser = async () => {
    if (!selectedUserId) return;
    if (!window.confirm('Delete this user?')) return;
    try {
      await deleteUser(selectedUserId);
      setUsers(users.filter((u) => u.id !== selectedUserId));
      await createAuditLog({ adminId: '1', actionType: 'delete_user', targetUserId: String(selectedUserId) });
      setMessage('User deleted and audit logged');
    } catch { setMessage('Failed to delete user'); }
  };

  const handleWarnUser = async () => {
    if (!selectedUserId) return;
    try {
      await createAuditLog({ adminId: '1', actionType: 'warning', targetUserId: String(selectedUserId) });
      setMessage('Warning issued and audit logged');
    } catch { setMessage('Failed to issue warning'); }
  };

  if (loading) return <div className="page"><p>Loading admin panel...</p></div>;

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Admin Panel</h1>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">User Management</h2>
        <select
          value={selectedUserId ?? ''}
          onChange={(e) => setSelectedUserId(Number(e.target.value))}
          style={{ width: '100%', marginBottom: '1rem' }}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>{u.name} ({u.email}) - Status: {u.accountStatus}</option>
          ))}
        </select>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button className="primary" onClick={handleGrantBadge}>Grant Verified Badge</button>
          <button className="secondary" onClick={handleRevokeBadge}>Revoke Verified Badge</button>
          <button className="secondary" onClick={handleWarnUser}>Warn User</button>
          <button style={{ background: 'var(--danger)', color: '#fff' }} onClick={handleDeleteUser}>Delete User</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Audit Log</h2>
        {auditLogs.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No audit logs recorded</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: 300, overflowY: 'auto' }}>
            {auditLogs.map((log) => (
              <div key={log.id} style={{ fontSize: '0.875rem', padding: '0.5rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-s)' }}>
                <strong>{log.actionType}</strong> by admin {log.adminId} on user {log.targetUserId}
              </div>
            ))}
          </div>
        )}
      </div>

      {message && <p style={{ color: message.includes('Failed') ? 'var(--danger)' : 'var(--success)' }}>{message}</p>}
    </div>
  );
}
