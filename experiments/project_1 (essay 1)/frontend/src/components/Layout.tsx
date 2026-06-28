import { NavLink } from 'react-router-dom'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <nav>
        <span style={{ fontWeight: 600, fontSize: '1.125rem', color: 'var(--text)' }}>
          Triage Dashboard
        </span>
        <NavLink to="/" style={{ fontWeight: 500 }}>Dashboard</NavLink>
        <NavLink to="/register" style={{ fontWeight: 500 }}>Register Patient</NavLink>
        <NavLink to="/queue" style={{ fontWeight: 500 }}>Queue</NavLink>
      </nav>
      <main className="page">
        {children}
      </main>
    </>
  )
}
