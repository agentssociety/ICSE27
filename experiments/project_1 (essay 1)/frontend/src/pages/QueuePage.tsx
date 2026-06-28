import { useState, useEffect, useCallback } from 'react'
import { getQueuePatients, dequeuePatient } from '../api/services'
import type { Patient } from '../types'
import UrgencyBadge from '../components/UrgencyBadge'

export default function QueuePage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dequeuing, setDequeuing] = useState(false)
  const [dequeueResult, setDequeueResult] = useState<string | null>(null)

  const fetchPatients = useCallback(async () => {
    try {
      const data = await getQueuePatients(1)
      setPatients(data)
      setError(null)
    } catch {
      setError('Failed to load queue. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchPatients()
  }, [fetchPatients])

  const handleDequeue = async () => {
    setDequeuing(true)
    setDequeueResult(null)
    try {
      const result = await dequeuePatient(1)
      if (result.patient) {
        setDequeueResult(`Dequeued patient: ${result.patient.patientId} (Urgency ${result.patient.urgency_level})`)
      } else {
        setDequeueResult('No patient available to dequeue.')
      }
      await fetchPatients()
    } catch {
      setDequeueResult('Failed to dequeue patient.')
    } finally {
      setDequeuing(false)
    }
  }

  return (
    <div>
      <h1>Queue Management</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        View the patient queue and dequeue the next highest-priority patient.
      </p>

      {error && (
        <div className="card" style={{ marginBottom: '1rem', color: 'var(--danger)', background: '#fff5f5' }}>
          {error}
        </div>
      )}

      {dequeueResult && (
        <div className="card" style={{ marginBottom: '1rem', background: 'var(--bg-secondary)' }}>
          {dequeueResult}
        </div>
      )}

      <div style={{ marginBottom: '1.5rem' }}>
        <button className="primary" onClick={handleDequeue} disabled={dequeuing || patients.length === 0}>
          {dequeuing ? 'Dequeuing…' : 'Dequeue Next Patient'}
        </button>
      </div>

      <h2 className="section-title">Queue ({patients.length} waiting)</h2>
      {loading ? (
        <p style={{ color: 'var(--text-secondary)' }}>Loading queue…</p>
      ) : patients.length === 0 ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)' }}>Queue is empty.</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: 'var(--bg-secondary)', textAlign: 'left' }}>
                <th style={{ padding: '0.75rem 1rem', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Patient ID</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Urgency</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Arrived</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: 600, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>State</th>
              </tr>
            </thead>
            <tbody>
              {patients.map((p) => (
                <tr key={p.id} style={{ borderTop: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.75rem 1rem', fontWeight: 500, fontFamily: 'monospace', fontSize: '0.875rem' }}>{p.patientId}</td>
                  <td style={{ padding: '0.75rem 1rem' }}><UrgencyBadge level={p.urgency_level} /></td>
                  <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                    {p.arrival_time ? new Date(p.arrival_time).toLocaleTimeString() : '—'}
                  </td>
                  <td style={{ padding: '0.75rem 1rem' }}>
                    <span className="badge">{p.state.replace('_', ' ')}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
