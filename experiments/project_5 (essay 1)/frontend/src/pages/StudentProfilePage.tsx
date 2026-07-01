import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStudent, getBadges, getAvatars, getRadarCharts, getNuggetWallets } from '../api/services';
import type { StudentResponse, BadgeResponse, AvatarResponse, RadarChartResponse, NuggetWalletResponse } from '../types';

export default function StudentProfilePage() {
  const [student, setStudent] = useState<StudentResponse | null>(null);
  const [badges, setBadges] = useState<BadgeResponse[]>([]);
  const [avatars, setAvatars] = useState<AvatarResponse[]>([]);
  const [radarChart, setRadarChart] = useState<RadarChartResponse | null>(null);
  const [nuggetWallet, setNuggetWallet] = useState<NuggetWalletResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');

  useEffect(() => {
    if (!studentId) {
      navigate('/student/register');
      return;
    }
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const [studentRes, badgesRes, avatarsRes, radarRes, walletRes] = await Promise.all([
          getStudent(studentId),
          getBadges(),
          getAvatars(),
          getRadarCharts(),
          getNuggetWallets()
        ]);
        setStudent(studentRes.data);
        setBadges(badgesRes.data);
        setAvatars(avatarsRes.data);
        setRadarChart(radarRes.data.length > 0 ? radarRes.data[0] : null);
        setNuggetWallet(walletRes.data.length > 0 ? walletRes.data[0] : null);
      } catch (err) {
        setError('Failed to load profile data.');
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [studentId, navigate]);

  if (loading) return <div className="page"><p>Loading profile...</p></div>;
  if (!student) return <div className="page"><p>Student not found. Please <a href="/student/register">register</a>.</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>My Profile</h1>
        <button className="secondary" onClick={() => navigate('/student/exam')}>Take Exam</button>
      </div>

      {error && (
        <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>
          {error}
        </div>
      )}

      {/* Profile Card */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <div style={{
            width: 80, height: 80, borderRadius: '50%',
            background: 'var(--bg-secondary)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '2rem'
          }}>
            {avatars.length > 0 ? '👤' : '👤'}
          </div>
          <div>
            <h2>{student.name}</h2>
            <p style={{ color: 'var(--text-secondary)' }}>{student.email}</p>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
              <span className="badge" style={{ background: 'var(--accent)', color: '#fff', fontSize: '0.9rem' }}>
                🪙 {Math.round(nuggetWallet?.balance ?? 0)} Nuggets
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Badges Section */}
      <section style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Earned Badges</h2>
        <div className="card">
          {badges.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No badges earned yet. Complete exams to earn badges!</p>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
              {badges.map(badge => (
                <div key={badge.id} style={{
                  background: 'var(--bg-secondary)', borderRadius: 'var(--radius-m)',
                  padding: '0.75rem 1rem', textAlign: 'center'
                }}>
                  <div style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }}>🏅</div>
                  <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{badge.name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{badge.description}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Competency Radar Chart */}
      <section style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Competency Radar</h2>
        <div className="card">
          {radarChart ? (
            <div>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>Your competency levels across skills:</p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '0.75rem' }}>
                {Object.entries(radarChart.competencies).map(([skill, level]) => (
                  <div key={skill} style={{ background: 'var(--bg-secondary)', borderRadius: 'var(--radius-s)', padding: '0.75rem', textAlign: 'center' }}>
                    <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.3rem' }}>{skill}</div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 700, color: level > 70 ? 'var(--success)' : level > 40 ? 'var(--warning)' : 'var(--danger)' }}>
                      {level}%
                    </div>
                    <div style={{
                      marginTop: '0.3rem', height: 4, background: 'var(--border-light)', borderRadius: 2, overflow: 'hidden'
                    }}>
                      <div style={{
                        height: '100%', width: `${level}%`, background: level > 70 ? 'var(--success)' : level > 40 ? 'var(--warning)' : 'var(--danger)',
                        borderRadius: 2, transition: 'width 0.5s ease'
                      }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-secondary)' }}>No competency data yet. Take exams to build your radar chart.</p>
          )}
        </div>
      </section>

      {/* Quick Actions */}
      <section>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="primary" onClick={() => navigate('/student/exam')}>Take an Exam</button>
          <button className="secondary" onClick={() => navigate('/student/rewards')}>Reward Store</button>
          <button className="secondary" onClick={() => navigate('/student/leaderboard')}>Leaderboard</button>
          <button className="secondary" onClick={() => navigate('/student/reviews')}>Past Reviews</button>
        </div>
      </section>
    </div>
  );
}
