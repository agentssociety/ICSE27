import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExamSessions, getExams, getQuestions, getCompetencyBreakdowns } from '../api/services';
import type { ExamSessionResponse, ExamResponse, QuestionResponse, CompetencyBreakdownResponse } from '../types';

export default function AttemptReviewPage() {
  const [sessions, setSessions] = useState<ExamSessionResponse[]>([]);
  const [exams, setExams] = useState<ExamResponse[]>([]);
  const [allQuestions, setAllQuestions] = useState<QuestionResponse[]>([]);
  const [breakdowns, setBreakdowns] = useState<Record<number, CompetencyBreakdownResponse[]>>({});
  const [selectedSession, setSelectedSession] = useState<ExamSessionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');

  useEffect(() => {
    if (!studentId) { navigate('/student/register'); return; }
    const fetchData = async () => {
      try {
        const [sessionsRes, examsRes, questionsRes] = await Promise.all([
          getExamSessions(), getExams(), getQuestions()
        ]);
        const mySessions = sessionsRes.data.filter(s => s.student_id === Number(studentId));
        setSessions(mySessions);
        setExams(examsRes.data);
        setAllQuestions(questionsRes.data);

        // Fetch breakdowns for each session
        const bds: Record<number, CompetencyBreakdownResponse[]> = {};
        await Promise.all(
          mySessions.map(async s => {
            try {
              const res = await getCompetencyBreakdowns(s.id);
              bds[s.id] = res.data;
            } catch {
              bds[s.id] = [];
            }
          })
        );
        setBreakdowns(bds);
      } catch {
        setError('Failed to load attempt data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [studentId, navigate]);

  if (!studentId) return null;

  const getExamTitle = (examId: number | null | undefined) => {
    if (!examId) return 'Unknown Exam';
    return exams.find(e => e.id === examId)?.title ?? `Exam #${examId}`;
  };

  const getSessionScore = (session: ExamSessionResponse) => {
    const questions = allQuestions.filter(q => q.exam_id === session.exam_id);
    if (questions.length === 0) return null;
    const correct = questions.filter(q => q.correct_answer && session.answers[String(q.id)] === q.correct_answer).length;
    return { correct, total: questions.length };
  };

  const getNuggetsEarned = (session: ExamSessionResponse) => {
    const questions = allQuestions.filter(q => q.exam_id === session.exam_id);
    return questions.reduce((sum, q) => {
      const isCorrect = q.correct_answer && session.answers[String(q.id)] === q.correct_answer;
      return sum + (isCorrect ? (q.nugget_reward_multiplier ?? 1) * 10 : 0);
    }, 0);
  };

  if (selectedSession) {
    const questions = allQuestions.filter(q => q.exam_id === selectedSession.exam_id);
    const sessionBreakdowns = breakdowns[selectedSession.id] ?? [];
    const score = getSessionScore(selectedSession);
    const nuggets = getNuggetsEarned(selectedSession);

    return (
      <div className="page">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <div>
            <h1>Attempt Review</h1>
            <p style={{ color: 'var(--text-secondary)' }}>{getExamTitle(selectedSession.exam_id)}</p>
          </div>
          <button className="secondary" onClick={() => setSelectedSession(null)}>Back to Attempts</button>
        </div>

        {/* Score Summary */}
        <div className="card" style={{ marginBottom: '1.5rem', display: 'flex', gap: '2rem', alignItems: 'center' }}>
          {score && (
            <div style={{ textAlign: 'center' }}>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Score</p>
              <p style={{ fontSize: '2rem', fontWeight: 700 }}>{score.correct}/{score.total}</p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{Math.round((score.correct / score.total) * 100)}%</p>
            </div>
          )}
          <div style={{ textAlign: 'center' }}>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Nuggets Earned</p>
            <p style={{ fontSize: '2rem', fontWeight: 700 }}>🪙 {Math.round(nuggets)}</p>
          </div>
        </div>

        {/* Competency Breakdown */}
        {sessionBreakdowns.length > 0 && (
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ marginBottom: '1rem' }}>Competency Breakdown</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {sessionBreakdowns.map(bd => {
                const pct = bd.max_score > 0 ? Math.round((bd.score / bd.max_score) * 100) : 0;
                return (
                  <div key={bd.id} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ minWidth: 150, fontSize: '0.9rem', fontWeight: 500 }}>{bd.competency_name}</span>
                    <div style={{ flex: 1, height: 8, background: 'var(--border-light)', borderRadius: 4, overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${pct}%`, background: bd.is_weak ? 'var(--danger)' : '#2ecc71', borderRadius: 4 }} />
                    </div>
                    <span style={{ minWidth: 40, fontSize: '0.85rem', color: bd.is_weak ? 'var(--danger)' : '#27ae60', textAlign: 'right' }}>{pct}%</span>
                    {bd.is_weak && <span style={{ fontSize: '0.8rem', color: 'var(--danger)' }}>⚠️</span>}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Per-Question Review */}
        <h3 style={{ marginBottom: '0.75rem' }}>Question Review</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {questions.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
              No questions found for this exam.
            </div>
          ) : (
            questions.map((q, i) => {
              const studentAnswer = selectedSession.answers[String(q.id)];
              const isCorrect = q.correct_answer && studentAnswer === q.correct_answer;
              const nuggetValue = (q.nugget_reward_multiplier ?? 1) * 10;
              return (
                <div key={q.id} className="card" style={{ borderLeft: `4px solid ${isCorrect ? '#2ecc71' : studentAnswer ? 'var(--danger)' : 'var(--border)'}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                      <strong>Q{i + 1}</strong>
                      <span className="badge">{q.type.replace(/_/g, ' ')}</span>
                      <span className="badge">{q.difficulty_tier}</span>
                    </div>
                    <span style={{ color: isCorrect ? '#27ae60' : 'var(--danger)', fontWeight: 600 }}>
                      {isCorrect ? `+${Math.round(nuggetValue)} 🪙` : studentAnswer ? '0 🪙' : 'Skipped'}
                    </span>
                  </div>
                  {q.body && <p style={{ marginBottom: '0.5rem', fontWeight: 500 }}>{q.body}</p>}
                  <div style={{ fontSize: '0.9rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.25rem' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Your answer:</span>
                      <span style={{ color: isCorrect ? '#27ae60' : studentAnswer ? 'var(--danger)' : 'var(--text-secondary)', fontWeight: 500 }}>
                        {studentAnswer || '(no answer)'}
                      </span>
                    </div>
                    {q.correct_answer && !isCorrect && (
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Correct answer:</span>
                        <span style={{ color: '#27ae60', fontWeight: 500 }}>{q.correct_answer}</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>My Attempts</h1>
        <button className="secondary" onClick={() => navigate('/student/profile')}>Back to Profile</button>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}

      {loading ? <p>Loading attempts...</p> : sessions.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>No attempts yet. Take an exam to see your results here!</p>
          <button className="primary" onClick={() => navigate('/student/exam')}>Take an Exam</button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {sessions.map(session => {
            const score = getSessionScore(session);
            const nuggets = getNuggetsEarned(session);
            const sessionBDs = breakdowns[session.id] ?? [];
            const weakCount = sessionBDs.filter(b => b.is_weak).length;
            return (
              <div key={session.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ marginBottom: '0.25rem' }}>{getExamTitle(session.exam_id)}</h3>
                  <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    {score && <span className="badge">{score.correct}/{score.total} correct</span>}
                    <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>🪙 +{Math.round(nuggets)}</span>
                    {weakCount > 0 && <span className="badge" style={{ background: '#ffe0e0', color: 'var(--danger)' }}>⚠️ {weakCount} weak competenc{weakCount === 1 ? 'y' : 'ies'}</span>}
                  </div>
                </div>
                <button className="primary" onClick={() => setSelectedSession(session)}>Review</button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
