import { useState } from 'react';

export default function LoginPage() {
  const [cardNumber, setCardNumber] = useState('');
  const [pin, setPin] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState<'success' | 'error' | 'info'>('info');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');

    if (!cardNumber || !pin) {
      setMessage('Please enter both card number and PIN.');
      setMessageType('error');
      return;
    }

    // Mock: In a real system, this would call the authentication endpoint
    setMessage('Authentication endpoint would be called here. Backend stub in progress.');
    setMessageType('info');
  };

  return (
    <div className="page" style={{ maxWidth: 480 }}>
      <h1 style={{ marginBottom: '0.5rem' }}>Card & PIN Login</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        Insert your card and enter your PIN to authenticate
      </p>

      <div className="card">
        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Card Number</label>
            <input
              type="text"
              value={cardNumber}
              onChange={e => setCardNumber(e.target.value)}
              placeholder="Enter card number"
            />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>PIN</label>
            <input
              type="password"
              value={pin}
              onChange={e => setPin(e.target.value)}
              placeholder="Enter PIN"
            />
          </div>
          <button type="submit" className="primary" style={{ width: '100%' }}>
            Authenticate
          </button>
        </form>
        {message && (
          <p style={{
            marginTop: '1rem',
            padding: '0.5rem',
            borderRadius: 'var(--radius-s)',
            background: messageType === 'error' ? 'var(--danger)' : messageType === 'success' ? 'var(--success)' : 'var(--bg-secondary)',
            color: messageType === 'info' ? 'var(--text)' : '#fff',
            fontSize: '0.85rem',
          }}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
