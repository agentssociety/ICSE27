import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getNuggetWallets, getRewardItems, createRedemption, getRedemptions } from '../api/services';
import type { NuggetWalletResponse, RewardItemResponse, RedemptionResponse } from '../types';

export default function RewardStorePage() {
  const [wallet, setWallet] = useState<NuggetWalletResponse | null>(null);
  const [rewardItems, setRewardItems] = useState<RewardItemResponse[]>([]);
  const [redemptions, setRedemptions] = useState<RedemptionResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [redeeming, setRedeeming] = useState<number | null>(null);
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');

  useEffect(() => {
    if (!studentId) return;
    const fetchData = async () => {
      try {
        const [walletRes, itemsRes, redemptionsRes] = await Promise.all([
          getNuggetWallets(Number(studentId)),
          getRewardItems(),
          getRedemptions(Number(studentId)),
        ]);
        setWallet(walletRes.data.length > 0 ? walletRes.data[0] : null);
        setRewardItems(itemsRes.data);
        setRedemptions(redemptionsRes.data);
      } catch {
        setError('Failed to load store data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [studentId]);

  const handleRedeem = async (item: RewardItemResponse) => {
    if (!wallet) { setMessage('No wallet found. Complete exams to earn nuggets!'); return; }
    if (wallet.balance < item.cost) { setMessage(`Insufficient nuggets. You need ${item.cost} but have ${Math.round(wallet.balance)}.`); return; }

    setRedeeming(item.id);
    setMessage('');
    try {
      await createRedemption({ student_id: Number(studentId), reward_item_id: item.id, nuggets_spent: item.cost });
      setWallet(prev => prev ? { ...prev, balance: prev.balance - item.cost } : null);
      const redemptionsRes = await getRedemptions(Number(studentId));
      setRedemptions(redemptionsRes.data);
      setMessage(`Successfully redeemed: ${item.name}!`);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setMessage(detail ?? 'Failed to redeem item.');
    } finally {
      setRedeeming(null);
    }
  };

  if (!studentId) {
    return <div className="page"><p>Please <a href="/student/register">register</a> first.</p></div>;
  }

  const alreadyRedeemed = new Set(redemptions.map(r => r.reward_item_id));

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Reward Store</h1>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span className="badge" style={{ background: 'var(--accent)', color: '#fff', fontSize: '1.1rem', padding: '0.4rem 1rem' }}>
            🪙 {Math.round(wallet?.balance ?? 0)} Nuggets
          </span>
          <button className="secondary" onClick={() => navigate('/student/profile')}>Back to Profile</button>
        </div>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}

      {message && (
        <div style={{
          background: message.startsWith('Successfully') ? '#e0ffe0' : '#ffe0e0',
          padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem',
          color: message.startsWith('Successfully') ? '#27ae60' : 'var(--danger)', fontSize: '0.9rem'
        }}>
          {message.startsWith('Successfully') ? '✅ ' : '❌ '}{message}
        </div>
      )}

      {loading ? <p>Loading store...</p> : (
        <>
          {rewardItems.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
              <p style={{ color: 'var(--text-secondary)' }}>No reward items available yet. Ask your instructor to add items.</p>
            </div>
          ) : (
            <>
              {/* Group by item_type */}
              {['virtual', 'badge', 'perk'].map(type => {
                const items = rewardItems.filter(i => (i.item_type ?? 'virtual') === type);
                if (items.length === 0) return null;
                return (
                  <section key={type} style={{ marginBottom: '2rem' }}>
                    <h2 className="section-title">{type.charAt(0).toUpperCase() + type.slice(1)} Rewards</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
                      {items.map(item => {
                        const isRedeemed = alreadyRedeemed.has(item.id);
                        const canAfford = (wallet?.balance ?? 0) >= item.cost;
                        return (
                          <div key={item.id} className="card" style={{ textAlign: 'center', opacity: isRedeemed ? 0.7 : 1 }}>
                            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
                              {type === 'badge' ? '🏅' : type === 'perk' ? '🎁' : '⭐'}
                            </div>
                            <h3 style={{ marginBottom: '0.25rem' }}>{item.name}</h3>
                            {item.description && <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>{item.description}</p>}
                            <p style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '1rem' }}>🪙 {item.cost} Nuggets</p>
                            <button
                              className={canAfford && !isRedeemed ? 'primary' : 'secondary'}
                              onClick={() => !isRedeemed && handleRedeem(item)}
                              disabled={isRedeemed || redeeming === item.id || !canAfford}
                            >
                              {isRedeemed ? '✓ Redeemed' : redeeming === item.id ? 'Redeeming...' : !canAfford ? 'Not enough nuggets' : 'Redeem'}
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                );
              })}

              {/* catch-all for other types */}
              {(() => {
                const knownTypes = new Set(['virtual', 'badge', 'perk']);
                const otherItems = rewardItems.filter(i => !knownTypes.has(i.item_type ?? 'virtual'));
                if (otherItems.length === 0) return null;
                return (
                  <section style={{ marginBottom: '2rem' }}>
                    <h2 className="section-title">Other Rewards</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
                      {otherItems.map(item => {
                        const isRedeemed = alreadyRedeemed.has(item.id);
                        const canAfford = (wallet?.balance ?? 0) >= item.cost;
                        return (
                          <div key={item.id} className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🎯</div>
                            <h3 style={{ marginBottom: '0.25rem' }}>{item.name}</h3>
                            {item.description && <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>{item.description}</p>}
                            <p style={{ fontWeight: 600, color: 'var(--accent)', marginBottom: '1rem' }}>🪙 {item.cost} Nuggets</p>
                            <button className={canAfford && !isRedeemed ? 'primary' : 'secondary'} onClick={() => !isRedeemed && handleRedeem(item)} disabled={isRedeemed || redeeming === item.id || !canAfford}>
                              {isRedeemed ? '✓ Redeemed' : redeeming === item.id ? 'Redeeming...' : !canAfford ? 'Not enough nuggets' : 'Redeem'}
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </section>
                );
              })()}
            </>
          )}

          {/* Redemption History */}
          {redemptions.length > 0 && (
            <section style={{ marginBottom: '2rem' }}>
              <h2 className="section-title">My Redemptions</h2>
              <div className="card">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {redemptions.map(r => {
                    const item = rewardItems.find(i => i.id === r.reward_item_id);
                    return (
                      <div key={r.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.4rem 0', borderBottom: '1px solid var(--border-light)' }}>
                        <span>{item?.name ?? `Item #${r.reward_item_id}`}</span>
                        <span style={{ color: 'var(--danger)' }}>-{r.nuggets_spent ?? item?.cost ?? 0} 🪙</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
