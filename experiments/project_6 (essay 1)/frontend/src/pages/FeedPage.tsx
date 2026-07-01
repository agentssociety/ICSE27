
import { useState, useEffect } from 'react';
import { listPosts, listUsers, createLike, deleteLike } from '../api/services';
import type { PostResponseDTO, UserResponse } from '../types';

export default function FeedPage() {
  const [posts, setPosts] = useState<PostResponseDTO[]>([]);
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([listPosts(), listUsers()])
      .then(([postsData, usersData]) => {
        setPosts(postsData.sort((a, b) => b.id - a.id));
        setUsers(usersData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const getUserName = (authorId: string) => {
    const user = users.find((u) => String(u.id) === authorId);
    return user?.name || `User #${authorId}`;
  };

  if (loading) return <div className="page"><p>Loading feed...</p></div>;
  if (error) return <div className="page"><p style={{ color: 'var(--danger)' }}>Error: {error}</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>News Feed</h1>
      </div>
      {posts.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No posts yet. Follow friends to see their posts!</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {posts.map((post) => (
            <div key={post.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <strong>{getUserName(post.authorId)}</strong>
                <span className="badge">Post #{post.id}</span>
              </div>
              <p style={{ marginBottom: '1rem', whiteSpace: 'pre-wrap' }}>{post.textContent}</p>
              <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.875rem' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Likes: 0</span>
                <span style={{ color: 'var(--text-secondary)' }}>Comments: 0</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
