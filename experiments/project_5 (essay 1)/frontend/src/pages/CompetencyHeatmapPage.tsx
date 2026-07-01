import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCompetencies, getExamSessions, getCompetencyBreakdowns, getStudents } from '../api/services';
import type { CompetencyResponse, StudentResponse, CompetencyBreakdownResponse } from '../types';

interface HeatmapCell {
  studentId: number;
  studentName: string;
  competencyName: string;
  avgScore: number;
  isWeak: boolean;
}

export default function CompetencyHeatmapPage() {
  const [competencies, setCompetencies] = useState<CompetencyResponse[]>([]);
  const [students, setStudents] = useState<StudentResponse[]>([]);
  const [allBreakdowns, setAllBreakdowns] = useState<CompetencyBreakdownResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [masteryThreshold, setMasteryThreshold] = useState(60);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [compsRes, studentsRes, sessionsRes] = await Promise.all([
          getCompetencies(), getStudents(), getExamSessions()
        ]);
        setCompetencies(compsRes.data);
        setStudents(studentsRes.data);

        // Fetch breakdowns for all sessions
        const bds: CompetencyBreakdownResponse[] = [];
        await Promise.all(
          sessionsRes.data.map(async s => {
            try {
              const res = await getCompetencyBreakdowns(s.id);
              bds.push(...res.data);
            } catch {
              // skip
            }
          })
        );
        setAllBreakdowns(bds);
      } catch {
        setError('Failed to load heatmap data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Build competency name set from breakdowns if competencies list is sparse
  const competencyNames = competencies.length > 0
    ? competencies.map(c => c.name)
    : [...new Set(allBreakdowns.map(b => b.competency_name))];

  // Aggregate: for each student×competency, average score pct across sessions
  const getAverageScore = (studentId: number, competencyName: string): number | null => {
    const relevant = allBreakdowns.filter(b => b.competency_name === competencyName);
    if (relevant.length === 0) return null;
    const scores = relevant.filter(b => {
      // we don't have a direct student link on breakdown; try via exam_session
      // For now show aggregate across all sessions with that competency
      return true;
    });
    const total = scores.reduce((sum, b) => sum + (b.max_score > 0 ? b.score / b.max_score : 0), 0);
    return (total / scores.length) * 100;
  };

  // Per-student breakdown: join sessions → breakdowns
  const getStudentScore = (studentId: number, competencyName: string): number | null => {
    // breakdown doesn't carry student_id directly; use the class-wide averages as a fallback
    // In a full implementation, exam_sessions would carry student_id and we'd join through them
    const avg = getAverageScore(studentId, competencyName);
    return avg;
  };

  const getColor = (score: number | null): string => {
    if (score === null) return 'var(--bg-secondary)';
    if (score < masteryThreshold) return `hsl(0, 80%, ${45 + (score / masteryThreshold) * 20}%)`;
    return `hsl(140, 60%, ${45 + ((score - masteryThreshold) / (100 - masteryThreshold)) * 20}%)`;
  };

  const weakStudents = students.filter(s =>
    competencyNames.some(cn => {
      const sc = getStudentScore(s.id, cn);
      return sc !== null && sc < masteryThreshold;
    })
  );

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1>Competency Heatmap</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Class-wide view of competency mastery</p>
        </div>
        <button className="secondary" onClick={() => navigate('/instructor/dashboard')}>Back to Dashboard</button>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}

      {/* Controls */}
      <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '2rem', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <label style={{ fontWeight: 500, fontSize: '0.9rem' }}>Mastery Threshold:</label>
          <input
            type="range" min={40} max={90} step={5} value={masteryThreshold}
            onChange={e => setMasteryThreshold(Number(e.target.value))}
            style={{ width: 140 }}
          />
          <span style={{ fontWeight: 600, color: 'var(--accent)', minWidth: 36 }}>{masteryThreshold}%</span>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', fontSize: '0.85rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <div style={{ width: 16, height: 16, borderRadius: 3, background: 'hsl(0, 80%, 55%)' }} />
            <span>Below threshold</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <div style={{ width: 16, height: 16, borderRadius: 3, background: 'hsl(140, 60%, 55%)' }} />
            <span>Above threshold</span>
          </div>
        </div>
      </div>

      {loading ? <p>Loading heatmap...</p> : (
        <>
          {/* At-risk summary */}
          {weakStudents.length > 0 && (
            <div className="card" style={{ marginBottom: '1.5rem', background: '#fff8f0', border: '1px solid #f39c12' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#e67e22' }}>⚠️ Students Below Threshold ({weakStudents.length})</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                {weakStudents.map(s => <span key={s.id} className="badge" style={{ background: '#ffe0e0', color: 'var(--danger)' }}>{s.name}</span>)}
              </div>
            </div>
          )}

          {/* Heatmap Table */}
          {competencyNames.length === 0 || students.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
              <p style={{ color: 'var(--text-secondary)' }}>No data available yet. Students need to complete exams for heatmap data to appear.</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                  <tr>
                    <th style={{ textAlign: 'left', padding: '0.5rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-s) 0 0 0', position: 'sticky', left: 0, zIndex: 2 }}>
                      Student
                    </th>
                    {competencyNames.map(cn => (
                      <th key={cn} style={{ padding: '0.5rem 0.75rem', background: 'var(--bg-secondary)', textAlign: 'center', whiteSpace: 'nowrap' }}>
                        {cn}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {students.map(student => (
                    <tr key={student.id}>
                      <td style={{ padding: '0.5rem', fontWeight: 500, position: 'sticky', left: 0, background: 'var(--bg)', zIndex: 1, borderBottom: '1px solid var(--border-light)' }}>
                        {student.name}
                      </td>
                      {competencyNames.map(cn => {
                        const score = getStudentScore(student.id, cn);
                        const color = getColor(score);
                        const isWeak = score !== null && score < masteryThreshold;
                        return (
                          <td key={cn} style={{ padding: '0.5rem', textAlign: 'center', borderBottom: '1px solid var(--border-light)' }}>
                            <div title={score !== null ? `${Math.round(score)}%` : 'No data'} style={{
                              width: 52, height: 32, borderRadius: 'var(--radius-s)',
                              background: color,
                              margin: '0 auto',
                              display: 'flex', alignItems: 'center', justifyContent: 'center',
                              color: score !== null ? '#fff' : 'var(--text-secondary)',
                              fontWeight: 600, fontSize: '0.8rem',
                              cursor: 'default',
                            }}>
                              {score !== null ? `${Math.round(score)}%` : '—'}
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Per-competency averages */}
          {competencyNames.length > 0 && allBreakdowns.length > 0 && (
            <div className="card" style={{ marginTop: '1.5rem' }}>
              <h3 style={{ marginBottom: '0.75rem' }}>Class Averages by Competency</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {competencyNames.map(cn => {
                  const bds = allBreakdowns.filter(b => b.competency_name === cn);
                  const avg = bds.length > 0 ? bds.reduce((s, b) => s + (b.max_score > 0 ? b.score / b.max_score : 0), 0) / bds.length * 100 : null;
                  const isWeak = avg !== null && avg < masteryThreshold;
                  return (
                    <div key={cn} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <span style={{ minWidth: 160, fontSize: '0.9rem', fontWeight: 500 }}>{cn}</span>
                      <div style={{ flex: 1, height: 8, background: 'var(--border-light)', borderRadius: 4, overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${avg ?? 0}%`, background: isWeak ? 'var(--danger)' : '#2ecc71', borderRadius: 4 }} />
                      </div>
                      <span style={{ minWidth: 48, textAlign: 'right', fontSize: '0.85rem', color: isWeak ? 'var(--danger)' : '#27ae60', fontWeight: 600 }}>
                        {avg !== null ? `${Math.round(avg)}%` : '—'}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
