import { useState, useEffect } from 'react';
import { listBloodUnits, listTransfusionRequests, getShortageAlerts, checkExpiredUnits } from '../api/services';
import type { BloodUnit, TransfusionRequest } from '../types';
import type { ShortageAlert } from '../api/services';

export default function DashboardPage() {
  const [units, setUnits] = useState<BloodUnit[]>([]);
  const [requests, setRequests] = useState<TransfusionRequest[]>([]);
  const [shortageAlerts, setShortageAlerts] = useState<ShortageAlert[]>([]);
  const [expiredUnits, setExpiredUnits] = useState<BloodUnit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [unitsData, requestsData, alerts, expired] = await Promise.all([
          listBloodUnits(),
          listTransfusionRequests(),
          getShortageAlerts(),
          checkExpiredUnits(),
        ]);
        setUnits(unitsData);
        setRequests(requestsData);
        setShortageAlerts(alerts);
        setExpiredUnits(expired);
      } catch (err) {
        setError('Failed to load dashboard data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="page"><p>Loading dashboard...</p></div>;
  if (error) return <div className="page"><p className="error">{error}</p></div>;

  // Compute stock levels
  const stockCounts: Record<string, { total: number; available: number }> = {};
  units.forEach(u => {
    if (!stockCounts[u.abo_rh_type]) stockCounts[u.abo_rh_type] = { total: 0, available: 0 };
    stockCounts[u.abo_rh_type].total++;
    if (!u.is_expired) stockCounts[u.abo_rh_type].available++;
  });

  // Units nearing expiration (within 5 days)
  const now = new Date();
  const nearExpiry = units.filter(u => {
    if (u.is_expired) return false;
    const collDate = new Date(u.collection_date);
    const expiryDate = new Date(collDate.getTime() + 42 * 24 * 60 * 60 * 1000); // 42 days shelf life
    const diffMs = expiryDate.getTime() - now.getTime();
    const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    return diffDays <= 5 && diffDays >= 0;
  });

  return (
    <div className="page">
      <h1>Inventory Dashboard</h1>

      {shortageAlerts.length > 0 && (
        <div className="card" style={{ borderColor: 'var(--warning)', marginBottom: '1rem' }}>
          <h2 className="section-title">Shortage Alerts</h2>
          {shortageAlerts.map(alert => (
            <p key={alert.abo_rh_type} style={{ color: 'var(--warning)' }}>
              Low stock: {alert.abo_rh_type} — only {alert.count} unit(s) remaining
            </p>
          ))}
        </div>
      )}

      <div className="card" style={{ marginBottom: '1rem' }}>
        <h2 className="section-title">Current Stock Levels</h2>
        {Object.keys(stockCounts).length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No blood units in inventory.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>Blood Type</th>
                <th style={{ padding: '0.5rem' }}>Total Units</th>
                <th style={{ padding: '0.5rem' }}>Available</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(stockCounts).map(([type, counts]) => (
                <tr key={type} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem' }}><strong>{type}</strong></td>
                  <td style={{ padding: '0.5rem' }}>{counts.total}</td>
                  <td style={{ padding: '0.5rem' }}>{counts.available}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card" style={{ marginBottom: '1rem' }}>
        <h2 className="section-title">Units Nearing Expiration</h2>
        {nearExpiry.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No units nearing expiration.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>Unit ID</th>
                <th style={{ padding: '0.5rem' }}>Type</th>
                <th style={{ padding: '0.5rem' }}>Collection Date</th>
                <th style={{ padding: '0.5rem' }}>Days Until Expiry</th>
              </tr>
            </thead>
            <tbody>
              {nearExpiry.map(u => {
                const collDate = new Date(u.collection_date);
                const expiryDate = new Date(collDate.getTime() + 42 * 24 * 60 * 60 * 1000);
                const diffMs = expiryDate.getTime() - now.getTime();
                const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
                return (
                  <tr key={u.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                    <td style={{ padding: '0.5rem' }}>{u.id}</td>
                    <td style={{ padding: '0.5rem' }}>{u.abo_rh_type}</td>
                    <td style={{ padding: '0.5rem' }}>{u.collection_date}</td>
                    <td style={{ padding: '0.5rem', color: diffDays <= 2 ? 'var(--danger)' : 'var(--warning)' }}>{diffDays} days</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h2 className="section-title">Open Transfusion Requests</h2>
        {requests.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)' }}>No open transfusion requests.</p>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '0.5rem' }}>Request ID</th>
                <th style={{ padding: '0.5rem' }}>Patient ID</th>
                <th style={{ padding: '0.5rem' }}>Blood Type</th>
                <th style={{ padding: '0.5rem' }}>Patient ABO/Rh</th>
                <th style={{ padding: '0.5rem' }}>Date</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(r => (
                <tr key={r.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                  <td style={{ padding: '0.5rem' }}>{r.requestId}</td>
                  <td style={{ padding: '0.5rem' }}>{r.patientId}</td>
                  <td style={{ padding: '0.5rem' }}>{r.bloodType}</td>
                  <td style={{ padding: '0.5rem' }}>{r.patientABORh}</td>
                  <td style={{ padding: '0.5rem' }}>{new Date().toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
