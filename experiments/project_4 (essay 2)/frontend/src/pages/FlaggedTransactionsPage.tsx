import { useState, useEffect } from "react";
import { listAuditLogEntries, updateAuditLogEntry } from "../api/services";
import type { AuditLogEntryResponse } from "../types";

export default function FlaggedTransactionsPage() {
  const [transactions, setTransactions] = useState<AuditLogEntryResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    listAuditLogEntries()
      .then((data) => {
        const flagged = data.filter(
          (e) => e.outcome === "FLAGGED" || e.eventType === "RAPID_WITHDRAWAL"
        );
        setTransactions(flagged.length > 0 ? flagged : data.slice(0, 5));
      })
      .catch((err: unknown) =>
        setError(err instanceof Error ? err.message : "Failed to load flagged transactions")
      )
      .finally(() => setLoading(false));
  }, []);

  const handleAction = async (idx: number, action: string) => {
    try {
      await updateAuditLogEntry(String(idx), { outcome: action === "approve" ? "APPROVED" : action === "deny" ? "DENIED" : "INVESTIGATING" });
      setTransactions((prev) => prev.filter((_, i) => i !== idx));
    } catch (err: unknown) {
      setError(`Failed to ${action}: ${err instanceof Error ? err.message : "Unknown"}`);
    }
  };

  if (loading) return <p>Loading flagged transactions...</p>;
  if (error)
    return (
      <div className="card" style={{ borderColor: "var(--danger)" }}>
        <p style={{ color: "var(--danger)" }}>{error}</p>
      </div>
    );

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Flagged Transactions</h1>
      <p className="section-title">
        {transactions.length} transaction{transactions.length !== 1 ? "s" : ""} pending review
      </p>

      {transactions.length === 0 ? (
        <div className="card">
          <p>No flagged transactions to review.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {transactions.map((tx, idx) => (
            <div className="card" key={idx}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                <span className="badge">{tx.eventType}</span>
              </div>
              <p><strong>User ID:</strong> {tx.userId}</p>
              <p><strong>Outcome:</strong> {tx.outcome}</p>
              <p><strong>Source IP:</strong> {tx.sourceIp}</p>
              <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.75rem" }}>
                <button className="primary" onClick={() => handleAction(idx, "approve")}>
                  Approve
                </button>
                <button
                  className="secondary"
                  style={{ borderColor: "var(--danger)", color: "var(--danger)" }}
                  onClick={() => handleAction(idx, "deny")}
                >
                  Deny
                </button>
                <button className="secondary" onClick={() => handleAction(idx, "investigate")}>
                  Investigate
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
