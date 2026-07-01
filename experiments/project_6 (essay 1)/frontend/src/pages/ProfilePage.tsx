
import { useState, useEffect } from 'react';
import { listUsers, listPosts } from '../api/services';
import type { UserResponse, PostResponseDTO } from '../types';

export default function ProfilePage() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [posts, setPosts] = useState<PostResponseDTO[]>([]);
  const [selectedUserId, setSelectedUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listUsers(), listPosts()])
      .then(([u, p]) => {
        setUsers(u);
        setPosts(p);
        if (u.length > 0) setSelectedUserId(u[0].id);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const userPosts = posts.filter((p) => String(p.authorId) === String(selectedUserId));
  const selectedUser = users.find((u) => u.id === selectedUserId);

  if (loading) return <div className="page"><p>Loading profile...</p></div>;

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Profile</h1>
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{ width: 80, height: 80, borderRadius: '50%', background: 'var(--bg-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem' }}>
            {selectedUser?.name?.charAt(0) || '?'}
          </div>
          <div style={{ flex: 1 }}>
            <h2>{selectedUser?.name || 'Select a user'}</h2>
            <p style={{ color: 'var(--text-secondary)' }}>{selectedUser?.email}</p>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
              <span className="badge">Status: {selectedUser?.accountStatus || 'N/A'}</span>
              <span className="badge">Posts: {userPosts.length}</span>
            </div>
          </div>
          <select 
            value={selectedUserId ?? ''} 
            onChange={(e) => setSelectedUserId(Number(e.target.value))}
            style={{ width: 'auto', minWidth: 180 }}
          >
            {users.map((u) => (
              <option key={u.id} value={u.id}>{u.name}</option>
            ))}
          </select>
        </div>
      </div>

      <h2 className="section-title">Post History</h2>
      {userPosts.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No posts yet</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {userPosts.map((post) => (
            <div key={post.id} className="card">
              <p style={{ whiteSpace: 'pre-wrap', marginBottom: '0.5rem' }}>{post.textContent}</p>
              <span className="badge">Post #{post.id}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
