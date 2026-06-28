import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registerPatient } from '../api/services'

export default function RegisterPatientPage() {
  const navigate = useNavigate()
  const [urgencyLevel, setUrgencyLevel] = useState(3)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await registerPatient({
        patientId: crypto.randomUUID(),
        urgency_level: urgencyLevel,
        state: 'pending_triage',
        patientQueue_id: 1,
      })
      navigate('/')
    } catch (err) {
      setError('Failed to register patient. Is the backend running?')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page">
      <h1>Register Patient</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        Assign an urgency level and add the patient to the triage queue.
      </p>

      {error && (
        <div className="card" style={{ marginBottom: '1rem', color: 'var(--danger)', background: '#fff5f5' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="card" style={{ maxWidth: 480 }}>
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.375rem', fontWeight: 500, fontSize: '0.9375rem', color: 'var(--text-secondary)' }}>
            Urgency Level
          </label>
          <select value={urgencyLevel} onChange={(e) => setUrgencyLevel(Number(e.target.value))}>
            <option value={1}>1 — Critical</option>
            <option value={2}>2 — High</option>
            <option value={3}>3 — Medium</option>
            <option value={4}>4 — Low</option>
            <option value={5}>5 — Routine</option>
          </select>
        </div>

        <button type="submit" className="primary" disabled={submitting}>
          {submitting ? 'Registering…' : 'Register Patient'}
        </button>
      </form>
    </div>
  )
}
