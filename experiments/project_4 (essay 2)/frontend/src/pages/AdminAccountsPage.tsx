import { useState, useEffect } from "react";
import { getUser, updateUser, unlockAccount } from "../api/services";
import type { UserResponse } from "../types";

export default function AdminAccountsPage() {
  const [users, setUsers] = useState<UserResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedUserId, setSelectedUserId] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  useEffect(() => {
    // Since there's no list users endpoint, we'll let the admin input user IDs manually
    setLoading(false);
  }, []);

  const handleLookupUser = async () => {
    if (!selectedUserId) return;
    setLoading(true);
    setError("");
    try {
      const user = await getUser(selectedUserId);
      setUsers((prev) => {
        const filtered = prev.filter((u) => u.id !== user.id);
        return [...filtered, user];
      });
    } catch (err: unknown) {
      setError(`User not found: ${err instanceof Error ? err.message : "Unknown"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleLock = async (userId: string) => {
    try {
      await updateUser(userId, { name: undefined, email: undefined });
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, is_active: false } : u))
      );
      setStatusMessage(`User ${userId} locked successfully`);
    } catch (err: unknown) {
      setStatusMessage(`Failed to lock: ${err instanceof Error ? err.message : "Unknown"}`);
    }
  };

  const handleUnlock = async (userId: string) => {
    try {
      const res = await unlockAccount({ userId, adminId: "admin-1" });
      if (res.success) {
        setUsers((prev) =>
          prev.map((u) => (u.id === userId ? { ...u, is_active: true } : u))
        );
        setStatusMessage(`User ${userId} unlocked successfully`);
      } else {
        setStatusMessage(`Failed to unlock: ${res.message}`);
      }
    } catch (err: unknown) {
      setStatusMessage(`Failed to unlock: ${err instanceof Error ? err.message : "Unknown"}`);
    }
  };

  if (loading) return <p>Loading user management...</p>;

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Admin - Account Management</h1>

      <div className="card" style={{ maxWidth: "500px", marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
          <input
            placeholder="Enter User ID"
            value={selectedUserId}
            onChange={(e) => setSelectedUserId(e.target.value)}
          />
          <button className="primary" onClick={handleLookupUser} disabled={loading}>
            Lookup
          </button>
        </div>
      </div>

      {error && (
        <div className="card" style={{ borderColor: "var(--danger)", marginBottom: "1.5rem" }}>
          <p style={{ color: "var(--danger)" }}>{error}</p>
        </div>
      )}

      {statusMessage && (
        <div className="card" style={{ marginBottom: "1.5rem" }}>
          <p>{statusMessage}</p>
        </div>
      )}

      {users.length === 0 ? (
        <div className="card">
          <p>No users loaded. Enter a User ID above to look up a user account.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {users.map((user) => (
            <div className="card" key={user.id}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
                <h3>{user.name}</h3>
                <span className="badge" style={{ background: user.is_active ? "var(--success)" : "var(--danger)", color: "#fff" }}>
                  {user.is_active ? "Active" : "Locked"}
                </span>
              </div>
              <p><strong>ID:</strong> {user.id}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.75rem" }}>
                {user.is_active ? (
                  <button
                    className="secondary"
                    style={{ borderColor: "var(--danger)", color: "var(--danger)" }}
                    onClick={() => handleLock(user.id)}
                  >
                    Lock Account
                  </button>
                ) : (
                  <button className="primary" onClick={() => handleUnlock(user.id)}>
                    Unlock Account
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
