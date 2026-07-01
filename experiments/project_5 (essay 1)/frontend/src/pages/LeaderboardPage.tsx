import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCohortLeaderboards, getStudents, getNuggetWallets } from '../api/services';
import type { CohortLeaderboardResponse, StudentResponse, NuggetWalletResponse } from '../types';

export default function LeaderboardPage() {
  const [leaderboard, setLeaderboard] = useState<CohortLeaderboardResponse[]>([]);
  const [students, setStudents] = useState<StudentResponse[]>([]);
  const [wallets, setWallets] = useState<NuggetWalletResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timeWindow, setTimeWindow] = useState('7');
  const [optedOut, setOptedOut] = useState(() => localStorage.getItem('leaderboard_opt_out') === 'true');
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');

  useEffect(() => {
    if (!studentId) return;
    const fetchData = async () => {
      try {
        const [lbRes, studentsRes, walletsRes] = await Promise.all([
          getCohortLeaderboards(), getStudents(), getNuggetWallets()
        ]);
        setLeaderboard(lbRes.data);
        setStudents(studentsRes.data);
        setWallets(walletsRes.data);
      } catch {
        setError('Failed to load leaderboard data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [studentId]);

  const handleOptOut = () => {
    const newValue = !optedOut;
    setOptedOut(newValue);
    localStorage.setItem('leaderboard_opt_out', String(newValue));
  };

  if (!studentId) {
    return <div className="page"><p>Please <a href="/student/register">register</a> first.</p></div>;
  }

  const getStudentNuggets = (sid: number | null | undefined) => {
    if (!sid) return 0;
    return wallets.find(w => w.student_id === sid)?.balance ?? 0;
  };

  const rankedStudents = leaderboard
    .map(entry => {
      const student = students.find(s => s.id === entry.student_id);
      return {
        id: entry.id,
        studentId: entry.student_id,
        name: student?.name || `Student #${entry.student_id}`,
        nuggets: getStudentNuggets(entry.student_id),
      };
    })
    .filter(entry => !(entry.studentId === Number(studentId) && optedOut))
    .sort((a, b) => b.nuggets - a.nuggets);

  const myRank = rankedStudents.findIndex(s => s.studentId === Number(studentId));

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Cohort Leaderboard</h1>
        <button className="secondary" onClick={() => navigate('/student/profile')}>Back to Profile</button>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}

      {/* Controls */}
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div>
            <label style={{ fontWeight: 500, marginRight: '0.5rem' }}>Time Window:</label>
            <select value={timeWindow} onChange={e => setTimeWindow(e.target.value)}>
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
              <option value="all">All time</option>
            </select>
          </div>
          <span className="badge">{rankedStudents.length} participants</span>
        </div>
        <button
          className={optedOut ? 'primary' : 'secondary'}
          onClick={handleOptOut}
          style={{ fontSize: '0.85rem' }}
        >
          {optedOut ? 'Re-join Leaderboard' : 'Opt Out'}
        </button>
      </div>

      {optedOut && (
        <div className="card" style={{ marginBottom: '1.5rem', background: 'rgba(0,113,227,0.04)', border: '1px solid var(--border)' }}>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            You have opted out of the leaderboard. Your rank is hidden from other students.
          </p>
        </div>
      )}

      {loading ? <p>Loading leaderboard...</p> : (
        <>
          {/* My Rank */}
          {myRank >= 0 && !optedOut && (
            <div className="card" style={{ marginBottom: '1.5rem', background: 'rgba(0,113,227,0.06)', border: '1px solid var(--accent)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent)' }}>#{myRank + 1}</span>
                  <div>
                    <strong>You</strong>
                    <span className="badge" style={{ marginLeft: '0.5rem' }}>🏆 {Math.round(rankedStudents[myRank]?.nuggets ?? 0)} nuggets</span>
                  </div>
                </div>
                {myRank <= 2 && <span style={{ fontSize: '2rem' }}>{['🥇', '🥈', '🥉'][myRank]}</span>}
              </div>
            </div>
          )}

          {/* Full Leaderboard */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {rankedStudents.length === 0 ? (
              <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
                <p style={{ color: 'var(--text-secondary)' }}>No leaderboard data available yet.</p>
              </div>
            ) : (
              rankedStudents.map((entry, index) => (
                <div key={entry.id} className="card" style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  border: entry.studentId === Number(studentId) ? '1px solid var(--accent)' : '1px solid var(--border-light)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span style={{ fontWeight: 700, fontSize: '1.1rem', minWidth: '2rem', color: index < 3 ? ['#ffd700', '#c0c0c0', '#cd7f32'][index] : 'var(--text-secondary)' }}>
                      #{index + 1}
                    </span>
                    <div>
                      <span style={{ fontWeight: 500 }}>{entry.name}</span>
                      {entry.studentId === Number(studentId) && <span className="badge" style={{ marginLeft: '0.5rem', background: 'var(--accent)', color: '#fff' }}>You</span>}
                      {index < 3 && <span style={{ marginLeft: '0.5rem' }}>{['🥇', '🥈', '🥉'][index]}</span>}
                    </div>
                  </div>
                  <span className="badge" style={{ background: 'var(--accent)', color: '#fff', fontSize: '0.9rem' }}>
                    🪙 {Math.round(entry.nuggets)}
                  </span>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
