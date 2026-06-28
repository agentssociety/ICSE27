import { useEffect, useState } from "react";
import { listReservations, createReservation, deleteReservation } from "../api/services";
import { ReservationResponse } from "../types";

const BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

const ReservationsPage = () => {
  const [reservations, setReservations] = useState<ReservationResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ bloodType: "O+", quantity: 1, scheduledDate: "" });

  useEffect(() => {
    listReservations()
      .then(setReservations)
      .catch(() => setError("Failed to load reservations"))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.scheduledDate) return;
    setSubmitting(true);
    try {
      const created = await createReservation({ ...form, quantity: Number(form.quantity) });
      setReservations((prev) => [created, ...prev]);
      setForm({ bloodType: "O+", quantity: 1, scheduledDate: "" });
    } catch {
      setError("Failed to create reservation");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteReservation(id);
      setReservations((prev) => prev.filter((r) => r.id !== id));
    } catch {
      setError("Failed to delete reservation");
    }
  };

  if (loading) return <div className="page"><div className="card">Loading...</div></div>;

  return (
    <div className="page">
      <h1>Reservations</h1>

      <div className="card" style={{ marginTop: "1.5rem", marginBottom: "1.5rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>New Reservation</h2>
        {error && <p style={{ color: "var(--danger)", marginBottom: "0.75rem" }}>{error}</p>}
        <form onSubmit={handleSubmit} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr auto", gap: "0.75rem", alignItems: "end" }}>
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
            <label style={{ display: "block", fontSize: "0.875rem", color: "var(--text-secondary)", marginBottom: "0.25rem" }}>Scheduled Date</label>
            <input
              type="date"
              value={form.scheduledDate}
              onChange={(e) => setForm((f) => ({ ...f, scheduledDate: e.target.value }))}
              required
            />
          </div>
          <button type="submit" className="primary" disabled={submitting}>{submitting ? "Reserving..." : "Reserve"}</button>
        </form>
      </div>

      {reservations.length === 0 ? (
        <div className="card"><p>No reservations yet.</p></div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Blood Type</th>
              <th>Quantity</th>
              <th>Scheduled Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td><strong>{r.bloodType}</strong></td>
                <td>{r.quantity}</td>
                <td>{r.scheduledDate}</td>
                <td><span className="badge">{r.status}</span></td>
                <td>
                  <button className="secondary" onClick={() => handleDelete(r.id)}>Cancel</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ReservationsPage;
