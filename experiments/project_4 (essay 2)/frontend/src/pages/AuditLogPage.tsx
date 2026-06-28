import { useState, useEffect } from "react";
import { listAuditLogEntries } from "../api/services";
import type { AuditLogEntryResponse } from "../types";

export default function AuditLogPage() {
  const [entries, setEntries] = useState<AuditLogEntryResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    listAuditLogEntries()
      .then((data) => setEntries(data))
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : "Failed to load audit log")
      )
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading audit log...</p>;
  if (error)
    return (
      <div className="card" style={{ borderColor: "var(--danger)" }}>
        <p style={{ color: "var(--danger)" }}>{error}</p>
      </div>
    );

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Audit Log</h1>
      <p className="section-title">
        {entries.length} security event{entries.length !== 1 ? "s" : ""} recorded
      </p>

      {entries.length === 0 ? (
        <div className="card">
          <p>No audit log entries found.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {entries.map((entry, idx) => (
            <div className="card" key={idx}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                <span className="badge">{entry.eventType}</span>
              </div>
              <p><strong>User:</strong> {entry.userId}</p>
              <p><strong>Source IP:</strong> {entry.sourceIp}</p>
              <p><strong>Outcome:</strong> {entry.outcome}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
