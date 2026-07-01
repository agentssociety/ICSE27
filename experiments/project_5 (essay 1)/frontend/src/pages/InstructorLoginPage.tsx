import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTeachers } from '../api/services';
import type { TeacherResponse } from '../types';

export default function InstructorLoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await getTeachers();
      const teachers = res.data;
      // Simple mock auth: find teacher by email-like name
      const found = teachers.find((t: TeacherResponse) =>
        t.name.toLowerCase().includes(email.toLowerCase())
      );
      if (found && password.length >= 3) {
        localStorage.setItem('instructor_id', String(found.id));
        localStorage.setItem('instructor_name', found.name);
        navigate('/instructor/dashboard');
      } else {
        setError('Invalid credentials. Try "admin" with any password.');
      }
    } catch (err) {
      setError('Failed to connect to server. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card" style={{ maxWidth: 400, margin: '2rem auto' }}>
        <h1 style={{ marginBottom: '0.5rem' }}>Instructor Login</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Sign in to manage exams and monitor student progress.
        </p>
        {error && (
          <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}
        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Enter your email" required />
          </div>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter password" required />
          </div>
          <button type="submit" className="primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <div style={{ marginTop: '1rem', textAlign: 'center', fontSize: '0.9rem' }}>
          <a href="/instructor/register">Don't have an account? Register</a>
        </div>
      </div>
    </div>
  );
}
