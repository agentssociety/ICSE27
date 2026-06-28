import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPatient } from '../api/services';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [symptoms, setSymptoms] = useState('');
  const [urgency, setUrgency] = useState('moderate');
  const [urgencyLevel, setUrgencyLevel] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUrgencyChange = (value: string) => {
    setUrgency(value);
    const map: Record<string, number> = { critical: 1, urgent: 2, moderate: 3, 'non-urgent': 4, minimal: 5 };
    setUrgencyLevel(map[value] || 3);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createPatient({
        symptoms,
        urgencyLevel,
        queuePosition: 0,
        arrivalTime: new Date().toISOString(),
        urgency,
      });
      alert('Patient registered successfully!');
      navigate('/queue');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to register patient');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="section-title">Register New Patient</h1>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
              Symptoms
            </label>
            <textarea
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              required
              placeholder="Describe patient symptoms..."
              rows={4}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
              Urgency Level
            </label>
            <select
              value={urgency}
              onChange={(e) => handleUrgencyChange(e.target.value)}
            >
              <option value="critical">1 - Critical</option>
              <option value="urgent">2 - Urgent</option>
              <option value="moderate">3 - Moderate</option>
              <option value="non-urgent">4 - Non-urgent</option>
              <option value="minimal">5 - Minimal</option>
            </select>
          </div>
          {error && <p style={{ color: 'var(--danger)', marginBottom: '1rem' }}>{error}</p>}
          <button className="primary" type="submit" disabled={loading}>
            {loading ? 'Registering...' : 'Register Patient'}
          </button>
        </form>
      </div>
    </div>
  );
}
