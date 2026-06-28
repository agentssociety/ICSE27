import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/services';

export default function LoginPage() {
  const navigate = useNavigate();
  const [cardId, setCardId] = useState('');
  const [pinId, setPinId] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const result = await loginUser({
        card_id: parseInt(cardId, 10),
        pin_id: parseInt(pinId, 10),
      });
      if (result.success && result.user) {
        navigate('/dashboard', { state: { user: result.user, account: result.account } });
      } else {
        setError(result.message || 'Login failed');
        if (result.locked) {
          setError(`Account locked: ${result.message}`);
        }
      }
    } catch {
      setError('An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', paddingTop: '3rem' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Card &amp; PIN Login</h2>
      <form onSubmit={handleLogin} className="card">
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.375rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Card ID</label>
          <input
            type="number"
            value={cardId}
            onChange={e => setCardId(e.target.value)}
            placeholder="Enter card ID"
            required
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.375rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>PIN ID</label>
          <input
            type="number"
            value={pinId}
            onChange={e => setPinId(e.target.value)}
            placeholder="Enter PIN ID"
            required
          />
        </div>
        {error && (
          <div style={{ color: 'var(--danger)', fontSize: '0.875rem', marginBottom: '0.75rem', padding: '0.5rem', background: 'rgba(255, 59, 48, 0.08)', borderRadius: 'var(--radius-s)' }}>
            {error}
          </div>
        )}
        <button type="submit" className="primary" disabled={loading} style={{ width: '100%', justifyContent: 'center' }}>
          {loading ? 'Authenticating...' : 'Login'}
        </button>
      </form>
    </div>
  );
}
