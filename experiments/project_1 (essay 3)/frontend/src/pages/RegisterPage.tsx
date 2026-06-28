import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPatient, createSymptom } from '../api/services';
import type { UrgencyLevel } from '../types';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [symptomDescription, setSymptomDescription] = useState('');
  const [symptomLanguage, setSymptomLanguage] = useState('en');
  const [urgency, setUrgency] = useState<UrgencyLevel>(1);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) {
      setError('Patient name is required.');
      return;
    }
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      // Create patient
      const patient = await createPatient({ username: username.trim(), authentication_id: 0 });
      
      // Create symptom with urgency embedded
      await createSymptom({
        description: `urgency:${urgency}\n${symptomDescription}`,
        language: symptomLanguage,
        patientId: String(patient.id),
        patient_id: patient.id,
      });

      setSuccess(`Patient "${username}" registered successfully with urgency level ${urgency}!`);
      setUsername('');
      setSymptomDescription('');
      setUrgency(1);
    } catch (err) {
      setError('Failed to register patient. Is the backend running?');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page">
      <h1 style={{ marginBottom: '1.5rem' }}>Register Patient</h1>

      {error && (
        <div className="card" style={{ background: '#fff2f0', border: '1px solid #ffccc7', marginBottom: '1rem', padding: '1rem' }}>
          <p style={{ color: 'var(--danger)' }}>{error}</p>
        </div>
      )}

      {success && (
        <div className="card" style={{ background: '#f6ffed', border: '1px solid #b7eb8f', marginBottom: '1rem', padding: '1rem' }}>
          <p style={{ color: 'var(--success)' }}>{success}</p>
        </div>
      )}

      <div className="card">
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Patient Name
            </label>
            <input
              type="text"
              placeholder="e.g. John Doe"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={submitting}
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
              Reported Symptoms
            </label>
            <textarea
              rows={3}
              placeholder="Describe the patient's symptoms..."
              value={symptomDescription}
              onChange={(e) => setSymptomDescription(e.target.value)}
              disabled={submitting}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                Language
              </label>
              <select value={symptomLanguage} onChange={(e) => setSymptomLanguage(e.target.value)} disabled={submitting}>
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                Initial Urgency Level
              </label>
              <select value={urgency} onChange={(e) => setUrgency(Number(e.target.value) as UrgencyLevel)} disabled={submitting}>
                <option value={1}>1 - Non-urgent</option>
                <option value={2}>2 - Low</option>
                <option value={3}>3 - Moderate</option>
                <option value={4}>4 - High</option>
                <option value={5}>5 - Critical</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
            <button type="submit" className="primary" disabled={submitting}>
              {submitting ? 'Registering...' : 'Register Patient'}
            </button>
            <button type="button" className="secondary" onClick={() => navigate('/')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
