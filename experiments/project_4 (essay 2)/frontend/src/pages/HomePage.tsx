import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div>
      <h1 style={{ marginBottom: "0.5rem" }}>Banking Security Dashboard</h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "2rem" }}>
        Manage authentication, monitor transactions, and control user access.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "1rem" }}>
        <Link to="/login" style={{ textDecoration: "none", color: "inherit" }}>
          <div className="card" style={{ cursor: "pointer", transition: "box-shadow 0.2s" }}>
            <h2 className="section-title">Card &amp; PIN Auth</h2>
            <p style={{ color: "var(--text-secondary)" }}>
              Authenticate with card and PIN, check balance, authorize transactions.
            </p>
          </div>
        </Link>

        <Link to="/audit-log" style={{ textDecoration: "none", color: "inherit" }}>
          <div className="card" style={{ cursor: "pointer", transition: "box-shadow 0.2s" }}>
            <h2 className="section-title">Audit Log</h2>
            <p style={{ color: "var(--text-secondary)" }}>
              View security events with precise timestamps and details.
            </p>
          </div>
        </Link>

        <Link to="/flagged-transactions" style={{ textDecoration: "none", color: "inherit" }}>
          <div className="card" style={{ cursor: "pointer", transition: "box-shadow 0.2s" }}>
            <h2 className="section-title">Flagged Transactions</h2>
            <p style={{ color: "var(--text-secondary)" }}>
              Review and act on suspicious transactions flagged by the system.
            </p>
          </div>
        </Link>

        <Link to="/admin/accounts" style={{ textDecoration: "none", color: "inherit" }}>
          <div className="card" style={{ cursor: "pointer", transition: "box-shadow 0.2s" }}>
            <h2 className="section-title">Admin: Accounts</h2>
            <p style={{ color: "var(--text-secondary)" }}>
              Lock/unlock user accounts and manage user access.
            </p>
          </div>
        </Link>
      </div>
    </div>
  );
}
