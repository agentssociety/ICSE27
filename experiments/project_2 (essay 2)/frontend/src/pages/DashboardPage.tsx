import { useState, useEffect } from 'react';
import { listBloodUnits, listTransfusionRequests } from '../api/services';
import type { BloodUnit, TransfusionRequestDTO } from '../types';

function groupByBloodType(units: BloodUnit[]) {
  const stock: Record<string, { aboType: string; rhFactor: string; total: number; available: number; expiringSoon: number }> = {};
  for (const unit of units) {
    const key = `${unit.aboType}${unit.rhFactor}`;
    if (!stock[key]) {
      stock[key] = { aboType: unit.aboType, rhFactor: unit.rhFactor, total: 0, available: 0, expiringSoon: 0 };
    }
    stock[key].total++;
    if (unit.status === 'available') {
      stock[key].available++;
    }
    const now = new Date();
    const expiry = new Date(unit.expiryDate);
    const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    if (daysUntilExpiry <= 7 && daysUntilExpiry >= 0) {
      stock[key].expiringSoon++;
    }
  }
  return Object.values(stock);
}

export default function DashboardPage() {
  const [bloodUnits, setBloodUnits] = useState<BloodUnit[]>([]);
  const [requests, setRequests] = useState<TransfusionRequestDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([listBloodUnits(), listTransfusionRequests()])
      .then(([units, reqs]) => {
        setBloodUnits(units);
        setRequests(reqs);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Failed to load dashboard data');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="page">
        <h1>Dashboard</h1>
        <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Loading dashboard data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page">
        <h1>Dashboard</h1>
        <div className="card" style={{ marginTop: '1rem', borderColor: 'var(--danger)' }}>
          <p style={{ color: 'var(--danger)' }}>Error: {error}</p>
          <button className="primary" style={{ marginTop: '1rem' }} onClick={() => window.location.reload()}>Retry</button>
        </div>
      </div>
    );
  }

  const stockLevels = groupByBloodType(bloodUnits);

  return (
    <div className="page">
      <h1>Blood Bank Dashboard</h1>
      <section style={{ marginTop: '2rem' }}>
        <h2 className="section-title">Stock Levels</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
          {stockLevels.map((s) => (
            <div key={`${s.aboType}${s.rhFactor}`} className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{s.aboType}{s.rhFactor}</div>
              <div style={{ fontSize: '2.5rem', fontWeight: 700, color: s.available <= 5 ? 'var(--danger)' : 'var(--accent)', margin: '0.5rem 0' }}>
                {s.available}
              </div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>available / {s.total} total</div>
              {s.expiringSoon > 0 && (
                <div className="badge" style={{ background: 'var(--warning)', color: '#fff', marginTop: '0.5rem' }}>
                  {s.expiringSoon} expiring soon
                </div>
              )}
            </div>
          ))}
          {stockLevels.length === 0 && <p style={{ color: 'var(--text-secondary)' }}>No blood units in inventory yet.</p>}
        </div>
      </section>

      {stockLevels.filter((s) => s.available < 5).length > 0 && (
        <section style={{ marginTop: '2rem' }}>
          <h2 className="section-title" style={{ color: 'var(--danger)' }}>Low Stock Alerts</h2>
          <div className="card" style={{ borderColor: 'var(--danger)' }}>
            {stockLevels.filter((s) => s.available < 5).map((s) => (
              <div key={`alert-${s.aboType}${s.rhFactor}`} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid var(--border-light)' }}>
                <span style={{ fontWeight: 600 }}>{s.aboType}{s.rhFactor}</span>
                <span style={{ color: 'var(--danger)' }}>{s.available} units remaining</span>
              </div>
            ))}
          </div>
        </section>
      )}

      <section style={{ marginTop: '2rem' }}>
        <h2 className="section-title">Open Transfusion Requests</h2>
        {requests.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No open transfusion requests.</p>
        ) : (
          <div className="card" style={{ padding: 0 }}>
            {requests.map((req, idx) => (
              <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-light)' }}>
                <div style={{ fontWeight: 600 }}>{req.bloodType}{req.rhFactor} - {req.quantity} unit(s)</div>
                <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>Pending</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
