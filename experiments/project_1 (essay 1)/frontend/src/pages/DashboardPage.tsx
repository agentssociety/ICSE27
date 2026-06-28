import { useState, useEffect, useCallback } from 'react'
import { getQueuePatients } from '../api/services'
import type { Patient } from '../types'
import UrgencyBadge from '../components/UrgencyBadge'

interface QueueStats {
  total: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

function computeStats(patients: Patient[]): QueueStats {
  return {
    total: patients.length,
    critical: patients.filter(p => p.urgency_level === 1).length,
    high: patients.filter(p => p.urgency_level === 2).length,
    medium: patients.filter(p => p.urgency_level === 3).length,
    low: patients.filter(p => p.urgency_level >= 4).length,
  }
}

export default function DashboardPage() {
  const [stats, setStats] = useState<QueueStats | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const patientsData = await getQueuePatients(1)
      setPatients(patientsData)
      setStats(computeStats(patientsData))
      setError(null)
    } catch (err) {
      setError('Failed to load dashboard data. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [fetchData])

  if (loading) {
    return (
      <div>
        <h1>Dashboard</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>Loading queue data…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div>
        <h1>Dashboard</h1>
        <div className="card" style={{ marginTop: '1rem', color: 'var(--danger)' }}>
          {error}
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
        Live queue overview — auto-refreshes every 10 seconds
      </p>

      {/* Overview cards */}
      {stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Total Waiting</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>{stats.total}</p>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Critical</p>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--danger)' }}>{stats.critical}</p>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>High</p>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--warning)' }}>{stats.high}</p>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Medium</p>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent)' }}>{stats.medium}</p>
          </div>
          <div className="card" style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Low</p>
            <p style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--text-secondary)' }}>{stats.low}</p>
          </div>
        </div>
      )}

      {/* Patient queue table */}
      <h2 className="section-title">Patient Queue</h2>
      {patients.length === 0 ? (
        <div className="card">
          <p style={{ color: 'var(--text-secondary)' }}>No patients in the queue.</p>
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
