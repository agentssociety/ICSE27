import { useEffect, useState } from "react";
import { listBloodUnits, createBloodUnit, deleteBloodUnit } from "../api/services";
import { BloodUnitResponse } from "../types";

const BLOOD_TYPES = ["A", "B", "AB", "O"];
const RH_FACTORS = ["+", "-"];

const BloodUnitsPage = () => {
  const [units, setUnits] = useState<BloodUnitResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ bloodType: "A", rhFactor: "+", donationDate: "" });

  useEffect(() => {
    listBloodUnits()
      .then(setUnits)
      .catch(() => setError("Failed to load blood units"))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.donationDate) return;
    setSubmitting(true);
    try {
      const created = await createBloodUnit(form);
      setUnits((prev) => [created, ...prev]);
      setForm({ bloodType: "A", rhFactor: "+", donationDate: "" });
    } catch {
      setError("Failed to add blood unit");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteBloodUnit(id);
      setUnits((prev) => prev.filter((u) => u.id !== id));
    } catch {
      setError("Failed to delete blood unit");
    }
  };

  if (loading) return <div className="page"><div className="card">Loading...</div></div>;

  return (
    <div className="page">
      <h1>Blood Units</h1>

      <div className="card" style={{ marginTop: "1.5rem", marginBottom: "1.5rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>Record New Unit</h2>
        {error && <p style={{ color: "var(--danger)", marginBottom: "0.75rem" }}>{error}</p>}
        <form onSubmit={handleSubmit} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr auto", gap: "0.75rem", alignItems: "end" }}>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Blood Type</label>
            <select value={form.bloodType} onChange={(e) => setForm((f) => ({ ...f, bloodType: e.target.value }))}>
              {BLOOD_TYPES.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Rh Factor</label>
            <select value={form.rhFactor} onChange={(e) => setForm((f) => ({ ...f, rhFactor: e.target.value }))}>
              {RH_FACTORS.map((r) => <option key={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Donation Date</label>
            <input type="date" value={form.donationDate} onChange={(e) => setForm((f) => ({ ...f, donationDate: e.target.value }))} required />
          </div>
          <button type="submit" className="primary" disabled={submitting}>{submitting ? "Adding..." : "Add Unit"}</button>
        </form>
      </div>

      {units.length === 0 ? (
        <div className="card"><p>No blood units recorded yet.</p></div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Blood Type</th>
              <th>Rh Factor</th>
              <th>Donation Date</th>
              <th>Expiration Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {units.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td><strong>{u.bloodType}</strong></td>
                <td>{u.rhFactor}</td>
                <td>{u.donationDate}</td>
                <td>{u.expirationDate ?? "—"}</td>
                <td>
                  {u.isExpiring
                    ? <span className="badge" style={{ background: "#fff3cd", color: "#856404" }}>Expiring Soon</span>
                    : <span className="badge" style={{ background: "#d4edda", color: "#155724" }}>Good</span>}
                </td>
                <td>
                  <button className="secondary" onClick={() => handleDelete(u.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default BloodUnitsPage;
