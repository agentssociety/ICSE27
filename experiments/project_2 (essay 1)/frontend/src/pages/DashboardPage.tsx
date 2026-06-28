import { useEffect, useState } from "react";
import { getInventoryDashboard } from "../api/services";
import { InventoryDashboard } from "../types";

const DashboardPage = () => {
  const [data, setData] = useState<InventoryDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getInventoryDashboard()
      .then(setData)
      .catch(() => setError("Failed to load dashboard"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page"><div className="card">Loading...</div></div>;
  if (error || !data) return <div className="page"><div className="card" style={{ color: "var(--danger)" }}>{error || "No data"}</div></div>;

  const stockEntries = Object.entries(data.stock_summary);

  return (
    <div className="page">
      <h1>Inventory Dashboard</h1>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem", marginTop: "1.5rem" }}>
        <div className="card" style={{ textAlign: "center" }}>
          <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}>Blood Types in Stock</p>
          <p style={{ fontSize: "2.5rem", fontWeight: 700 }}>{stockEntries.length}</p>
        </div>
        <div className="card" style={{ textAlign: "center" }}>
          <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}>Expiring Soon</p>
          <p style={{ fontSize: "2.5rem", fontWeight: 700, color: data.expiring_units_count > 0 ? "var(--warning)" : undefined }}>
            {data.expiring_units_count}
          </p>
        </div>
        <div className="card" style={{ textAlign: "center" }}>
          <p style={{ fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}>Pending Requests</p>
          <p style={{ fontSize: "2.5rem", fontWeight: 700, color: data.pending_requests_count > 0 ? "var(--accent)" : undefined }}>
            {data.pending_requests_count}
          </p>
        </div>
      </div>

      <div className="card" style={{ marginTop: "1.5rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>Stock by Blood Type</h2>
        {stockEntries.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>No stock recorded yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Blood Type</th>
                <th>Units Available</th>
              </tr>
            </thead>
            <tbody>
              {stockEntries.map(([type, count]) => (
                <tr key={type}>
                  <td><strong>{type}</strong></td>
                  <td>{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {data.expiring_units_count > 0 && (
        <div className="card" style={{ marginTop: "1rem" }}>
          <h2 style={{ marginBottom: "1rem", color: "var(--warning)" }}>Expiring Units (within 7 days)</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Blood Type</th>
                <th>Rh Factor</th>
                <th>Expiration Date</th>
              </tr>
            </thead>
            <tbody>
              {data.expiring_units.map((u) => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td><strong>{u.bloodType}</strong></td>
                  <td>{u.rhFactor}</td>
                  <td style={{ color: "var(--warning)" }}>{u.expirationDate ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
