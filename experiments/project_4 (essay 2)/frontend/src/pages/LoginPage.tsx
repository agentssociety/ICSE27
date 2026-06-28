import { useState } from "react";
import { login, getBalance, authorizeTransaction, unlockAccount } from "../api/services";
import type { LoginResponseDTO, AccountData } from "../types";

export default function LoginPage() {
  const [userId, setUserId] = useState("");
  const [pin, setPin] = useState("");
  const [result, setResult] = useState<LoginResponseDTO | null>(null);
  const [balance, setBalance] = useState<AccountData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [amount, setAmount] = useState("");
  const [authResult, setAuthResult] = useState("");

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await login({ userId, pin });
      setResult(res);
      if (res.success) {
        // Fetch balance on successful login
        const bal = await getBalance(userId);
        setBalance(bal);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleAuthorize = async () => {
    if (!balance || !amount) return;
    try {
      const res = await authorizeTransaction({
        initiatorId: userId,
        accountId: userId,
        amount: parseInt(amount),
        permission: "WITHDRAWAL",
        interfaceType: "ATM",
      });
      setAuthResult(res.authorized ? "Authorized!" : `Denied: ${res.reason}`);
      if (res.authorized) {
        setBalance({ balance: res.newBalance, dailyLimit: balance.dailyLimit, usedToday: res.newUsedToday });
      }
    } catch (err: unknown) {
      setAuthResult(`Error: ${err instanceof Error ? err.message : "Unknown"}`);
    }
  };

  const handleUnlock = async () => {
    setLoading(true);
    try {
      const res = await unlockAccount({ userId, adminId: "admin-1" });
      if (res.success) {
        setResult({ success: true, lockStatus: "UNLOCKED", message: "Account unlocked by admin" });
      }
    } catch (err: unknown) {
      setError(`Unlock error: ${err instanceof Error ? err.message : "Unknown"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: "1.5rem" }}>Card &amp; PIN Authentication</h1>

      <div className="card" style={{ maxWidth: "400px", marginBottom: "1.5rem" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          <input
            placeholder="User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <input
            type="password"
            placeholder="PIN"
            value={pin}
            onChange={(e) => setPin(e.target.value)}
          />
          <button className="primary" onClick={handleLogin} disabled={loading}>
            {loading ? "Authenticating..." : "Login"}
          </button>
        </div>
      </div>

      {error && (
        <div className="card" style={{ borderColor: "var(--danger)", marginBottom: "1.5rem" }}>
          <p style={{ color: "var(--danger)" }}>{error}</p>
        </div>
      )}

      {result && (
        <div className="card" style={{ marginBottom: "1.5rem" }}>
          <p>
            <strong>Status:</strong>{" "}
            <span style={{ color: result.success ? "var(--success)" : "var(--danger)" }}>
              {result.success ? "Authenticated" : "Failed"}
            </span>
          </p>
          <p><strong>Lock Status:</strong> {result.lockStatus}</p>
          <p><strong>Message:</strong> {result.message}</p>
        </div>
      )}

      {result?.lockStatus === "LOCKED" && (
        <div className="card" style={{ marginBottom: "1.5rem", borderColor: "var(--warning)" }}>
          <p style={{ marginBottom: "0.75rem" }}>
            Your account is locked due to multiple failed attempts.
          </p>
          <button className="secondary" onClick={handleUnlock} disabled={loading}>
            Request Admin Unlock
          </button>
        </div>
      )}

      {balance && (
        <div className="card" style={{ marginBottom: "1.5rem" }}>
          <h2 className="section-title">Account Balance</h2>
          <p><strong>Balance:</strong> ${balance.balance}</p>
          <p><strong>Daily Limit:</strong> ${balance.dailyLimit}</p>
          <p><strong>Used Today:</strong> ${balance.usedToday}</p>

          <div style={{ marginTop: "1rem", display: "flex", gap: "0.5rem", alignItems: "center" }}>
            <input
              type="number"
              placeholder="Amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              style={{ maxWidth: "150px" }}
            />
            <button className="primary" onClick={handleAuthorize}>
              Authorize Transaction
            </button>
          </div>
          {authResult && (
            <p style={{ marginTop: "0.5rem", color: authResult.startsWith("Authorized") ? "var(--success)" : "var(--danger)" }}>
              {authResult}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
