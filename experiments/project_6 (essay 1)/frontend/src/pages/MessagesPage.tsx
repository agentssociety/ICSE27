
import { useState, useEffect } from 'react';
import axios from 'axios';
import { listUsers } from '../api/services';

export default function MessagesPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/messages').then(r => setMessages(r.data))
      .catch(() => {}).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page"><p>Loading messages...</p></div>;

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Messages</h1>
      {messages.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-secondary)' }}>No messages yet. Visit a user profile to send a message.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {messages.map((m: any) => (
            <div key={m.id} className="card">
              <p>Message #{m.id}</p>
              <span className="badge">Direct Message</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
