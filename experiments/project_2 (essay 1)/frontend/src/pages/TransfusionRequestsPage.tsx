import { useEffect, useState } from "react";
import { listTransfusionRequests, createTransfusionRequest, deleteTransfusionRequest } from "../api/services";
import { TransfusionRequestResponse } from "../types";

const BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];
const URGENCY_LEVELS = ["routine", "urgent", "emergency"];

const urgencyColor: Record<string, { background: string; color: string }> = {
  routine: { background: "#d4edda", color: "#155724" },
  urgent: { background: "#fff3cd", color: "#856404" },
  emergency: { background: "#f8d7da", color: "#721c24" },
};

const TransfusionRequestsPage = () => {
  const [requests, setRequests] = useState<TransfusionRequestResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ patientName: "", bloodType: "O+", quantity: 1, urgency: "routine" });

  useEffect(() => {
    listTransfusionRequests()
      .then(setRequests)
      .catch(() => setError("Failed to load transfusion requests"))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.patientName.trim()) return;
    setSubmitting(true);
    try {
      const created = await createTransfusionRequest({ ...form, quantity: Number(form.quantity) });
      setRequests((prev) => [created, ...prev]);
      setForm({ patientName: "", bloodType: "O+", quantity: 1, urgency: "routine" });
    } catch {
      setError("Failed to create transfusion request");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteTransfusionRequest(id);
      setRequests((prev) => prev.filter((r) => r.id !== id));
    } catch {
      setError("Failed to delete request");
    }
  };

  if (loading) return <div className="page"><div className="card">Loading...</div></div>;

  return (
    <div className="page">
      <h1>Transfusion Requests</h1>

      <div className="card" style={{ marginTop: "1.5rem", marginBottom: "1.5rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>New Request</h2>
        {error && <p style={{ color: "var(--danger)", marginBottom: "0.75rem" }}>{error}</p>}
        <form onSubmit={handleSubmit} style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr auto", gap: "0.75rem", alignItems: "end" }}>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Patient Name</label>
            <input
              type="text"
              placeholder="Patient name"
              value={form.patientName}
              onChange={(e) => setForm((f) => ({ ...f, patientName: e.target.value }))}
              required
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Blood Type</label>
            <select value={form.bloodType} onChange={(e) => setForm((f) => ({ ...f, bloodType: e.target.value }))}>
              {BLOOD_TYPES.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Quantity (units)</label>
            <input
              type="number"
              min={1}
              value={form.quantity}
              onChange={(e) => setForm((f) => ({ ...f, quantity: Number(e.target.value) }))}
              required
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Urgency</label>
            <select value={form.urgency} onChange={(e) => setForm((f) => ({ ...f, urgency: e.target.value }))}>
              {URGENCY_LEVELS.map((u) => <option key={u}>{u}</option>)}
            </select>
          </div>
          <button type="submit" className="primary" disabled={submitting}>{submitting ? "Submitting..." : "Submit"}</button>
        </form>
      </div>

      {requests.length === 0 ? (
        <div className="card"><p>No transfusion requests yet.</p></div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Patient</th>
              <th>Blood Type</th>
              <th>Quantity</th>
              <th>Urgency</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.patientName}</td>
                <td><strong>{r.bloodType}</strong></td>
                <td>{r.quantity}</td>
                <td>
                  <span className="badge" style={urgencyColor[r.urgency] ?? {}}>
                    {r.urgency}
                  </span>
                </td>
                <td>
                  <span className="badge">{r.status}</span>
                </td>
                <td>
                  <button className="secondary" onClick={() => handleDelete(r.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TransfusionRequestsPage;
