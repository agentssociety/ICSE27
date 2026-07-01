
import { useState, useEffect } from 'react';
import { listNotifications, listUsers } from '../api/services';
import type { NotificationResponse, UserResponse } from '../types';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listNotifications(), listUsers()])
      .then(([n, u]) => {
        setNotifications(n);
        setUsers(u);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const getUserName = (userId: number | undefined) => {
    if (!userId) return 'System';
    const user = users.find((u) => u.id === userId);
    return user?.name || `User #${userId}`;
  };

  if (loading) return <div className="page"><p>Loading notifications...</p></div>;

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Notifications</h1>
      {notifications.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No notifications yet</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {notifications.map((n) => (
            <div key={n.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <p>
                  {n.like_id ? `Someone liked your post` : n.comment_id ? `Someone commented on your post` : `Notification #${n.id}`}
                </p>
                <span className="badge" style={{ marginTop: '0.25rem' }}>ID: {n.id}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
