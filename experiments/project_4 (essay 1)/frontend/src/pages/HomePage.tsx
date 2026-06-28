import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div>
      <div style={{ textAlign: 'center', paddingTop: '4rem', paddingBottom: '2rem' }}>
        <h1>ATM Banking System</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem', fontSize: '1.125rem' }}>
          Secure card &amp; PIN authentication with fraud detection
        </p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', maxWidth: '800px', margin: '0 auto' }}>
        <Link to="/login" style={{ textDecoration: 'none' }}>
          <div className="card" style={{ cursor: 'pointer', transition: 'transform var(--ease), box-shadow var(--ease)' }}
               onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = 'var(--shadow-m)'; }}
               onMouseLeave={e => { e.currentTarget.style.transform = ''; e.currentTarget.style.boxShadow = ''; }}>
            <h2>User Login</h2>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              Authenticate with your card and PIN to access your account.
            </p>
          </div>
        </Link>
        <Link to="/admin/accounts" style={{ textDecoration: 'none' }}>
          <div className="card" style={{ cursor: 'pointer', transition: 'transform var(--ease), box-shadow var(--ease)' }}
               onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = 'var(--shadow-m)'; }}
               onMouseLeave={e => { e.currentTarget.style.transform = ''; e.currentTarget.style.boxShadow = ''; }}>
            <h2>Admin Panel</h2>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
              Manage accounts, review flagged transactions, and view audit logs.
            </p>
          </div>
        </Link>
      </div>
    </div>
  );
}
