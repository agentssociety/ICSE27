
import { useState, useEffect } from 'react';
import { listNotificationPreferences, createNotificationPreference, listUsers, updateUser, deleteUser } from '../api/services';
import type { NotificationPreferenceResponse, UserResponse } from '../types';

export default function SettingsPage() {
  const [prefs, setPrefs] = useState<NotificationPreferenceResponse[]>([]);
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    Promise.all([listNotificationPreferences(), listUsers()])
      .then(([p, u]) => {
        setPrefs(p);
        setUsers(u);
        if (u.length > 0) setSelectedUserId(u[0].id);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const togglePref = async () => {
    if (!selectedUserId) return;
    try {
      await createNotificationPreference({ userId: String(selectedUserId), enabled: true });
      setMessage('Notification preference updated');
    } catch {
      setMessage('Failed to update preference');
    }
  };

  const handleDeleteAccount = async () => {
    if (!selectedUserId) return;
    if (!window.confirm('Are you sure you want to delete this account? This is irreversible.')) return;
    try {
      await deleteUser(selectedUserId);
      setMessage('Account deleted');
      setUsers(users.filter((u) => u.id !== selectedUserId));
      setSelectedUserId(users.length > 1 ? users[0].id : null);
    } catch {
      setMessage('Failed to delete account');
    }
  };

  if (loading) return <div className="page"><p>Loading settings...</p></div>;

  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <h1 style={{ marginBottom: '1.5rem' }}>Settings</h1>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Select User</h2>
        <select
          value={selectedUserId ?? ''}
          onChange={(e) => setSelectedUserId(Number(e.target.value))}
          style={{ width: '100%' }}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>{u.name} ({u.email})</option>
          ))}
        </select>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Notification Preferences</h2>
        {prefs.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No notification preferences configured</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {prefs.map((pref) => (
              <div key={pref.userId} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>User {pref.userId}: Notifications {pref.enabled ? 'Enabled' : 'Disabled'}</span>
                <button className="secondary" onClick={togglePref} style={{ padding: '0.3rem 0.75rem', fontSize: '0.8125rem' }}>
                  Toggle
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2 className="section-title">Account Management</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Manage your account settings for the selected user.
        </p>
        <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <button className="secondary" onClick={() => setMessage('Change password feature (backend implementation needed)')}>
            Change Password
          </button>
          <button className="secondary" onClick={() => setMessage('Change email feature (backend implementation needed)')}>
            Change Email
          </button>
          <button style={{ background: 'var(--danger)', color: '#fff' }} onClick={handleDeleteAccount}>
            Delete Account
          </button>
        </div>
        {message && <p style={{ marginTop: '0.75rem', fontSize: '0.875rem', color: message.includes('Failed') ? 'var(--danger)' : 'var(--success)' }}>{message}</p>}
      </div>
    </div>
  );
}
