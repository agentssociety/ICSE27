
import { useState } from 'react';
import { listPosts, listUsers } from '../api/services';
import type { PostResponseDTO, UserResponse } from '../types';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [allPosts, setAllPosts] = useState<PostResponseDTO[]>([]);
  const [allUsers, setAllUsers] = useState<UserResponse[]>([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const [posts, users] = await Promise.all([listPosts(), listUsers()]);
      setAllPosts(posts);
      setAllUsers(users);
    } catch {}
    setSearched(true);
    setLoading(false);
  };

  const filteredPosts = allPosts.filter((p) =>
    p.textContent.toLowerCase().includes(query.toLowerCase())
  );
  const filteredUsers = allUsers.filter((u) =>
    u.name.toLowerCase().includes(query.toLowerCase()) || u.email.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Search</h1>
      <div className="card" style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Search users and posts..."
          style={{ flex: 1 }}
        />
        <button className="primary" onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {searched && (
        <>
          <h2 className="section-title">Users ({filteredUsers.length})</h2>
          {filteredUsers.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>No users found</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
              {filteredUsers.map((u) => (
                <div key={u.id} className="card" style={{ padding: '0.75rem 1rem' }}>
                  <strong>{u.name}</strong>
                  <span className="badge" style={{ marginLeft: '0.5rem' }}>User</span>
                  <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{u.email}</p>
                </div>
              ))}
            </div>
          )}

          <h2 className="section-title">Posts ({filteredPosts.length})</h2>
          {filteredPosts.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No posts found</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {filteredPosts.map((p) => (
                <div key={p.id} className="card" style={{ padding: '0.75rem 1rem' }}>
                  <p>{p.textContent}</p>
                  <span className="badge">Post #{p.id}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
