import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getExams, getQuestions, createExamSession, getStreaks, getNuggetWallets,
  createNuggetWallet, updateNuggetWallet,
  getSchedules, recordCorrectAnswer, recordWrongAnswer, createCompetencyBreakdown,
} from '../api/services';
import type { ExamResponse, QuestionResponse, StreakResponse, NuggetWalletResponse, ScheduleResponse } from '../types';

export default function TakeExamPage() {
  const [exams, setExams] = useState<ExamResponse[]>([]);
  const [questions, setQuestions] = useState<QuestionResponse[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedExam, setSelectedExam] = useState<ExamResponse | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [showResult, setShowResult] = useState(false);
  const [showBreakdown, setShowBreakdown] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timer, setTimer] = useState(0);
  const [streak, setStreak] = useState<StreakResponse | null>(null);
  const [wallet, setWallet] = useState<NuggetWalletResponse | null>(null);
  const [nuggetCount, setNuggetCount] = useState(0);
  const [animatingNugget, setAnimatingNugget] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const timerRef = useRef<number | null>(null);
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');

  useEffect(() => {
    if (!studentId) {
      navigate('/student/register');
      return;
    }
    const fetchData = async () => {
      try {
        const [examsRes, streaksRes, walletsRes] = await Promise.all([
          getExams(),
          getStreaks(Number(studentId)),
          getNuggetWallets(Number(studentId)),
        ]);
        setExams(examsRes.data);
        if (streaksRes.data.length > 0) setStreak(streaksRes.data[0]);
        if (walletsRes.data.length > 0) {
          setWallet(walletsRes.data[0]);
          setNuggetCount(walletsRes.data[0].balance);
        }
      } catch {
        setError('Failed to load exam data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [studentId, navigate]);

  // Timer countdown
  useEffect(() => {
    if (selectedExam && !showResult && timer > 0) {
      timerRef.current = window.setInterval(() => {
        setTimer(prev => {
          if (prev <= 1) {
            if (timerRef.current) clearInterval(timerRef.current);
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => {
        if (timerRef.current) clearInterval(timerRef.current);
      };
    }
  }, [selectedExam, showResult]);

  const handleSelectExam = async (exam: ExamResponse) => {
    setSelectedExam(exam);
    setShowResult(false);
    setCurrentQuestionIndex(0);
    setAnswers({});

    // Fetch questions for this exam
    const questionsRes = await getQuestions(exam.id);
    setQuestions(questionsRes.data);

    // Fetch schedule time limit for this exam
    const schedulesRes = await getSchedules();
    const examSchedule = schedulesRes.data.find(s => s.exam_id === String(exam.id));
    const timeLimitSecs = examSchedule?.per_attempt_time_limit_minutes
      ? examSchedule.per_attempt_time_limit_minutes * 60
      : 600;
    setTimer(timeLimitSecs);
  };

  const currentMultiplier = streak?.multiplier ?? 1;

  const handleAnswer = (questionId: number, answer: string) => {
    setAnswers(prev => ({ ...prev, [String(questionId)]: answer }));
  };

  const handleNextQuestion = async () => {
    const current = questions[currentQuestionIndex];
    if (current && streak) {
      const isCorrect = current.correct_answer
        ? answers[String(current.id)] === current.correct_answer
        : false;
      if (isCorrect) {
        const updated = await recordCorrectAnswer(streak.id).catch(() => null);
        if (updated) setStreak(updated.data);
      } else if (answers[String(current.id)]) {
        const updated = await recordWrongAnswer(streak.id).catch(() => null);
        if (updated) setStreak(updated.data);
      }
    }

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setShowResult(true);

    const earnedNuggets = questions.reduce((sum, q) => {
      const baseReward = (q.nugget_reward_multiplier ?? 1) * 10;
      const isCorrect = q.correct_answer && answers[String(q.id)] === q.correct_answer;
      return sum + (isCorrect ? baseReward * currentMultiplier : 0);
    }, 0);

    setNuggetCount(prev => prev + earnedNuggets);
    setAnimatingNugget(true);
    setTimeout(() => setAnimatingNugget(false), 1500);

    // Persist nuggets to the backend wallet
    try {
      if (earnedNuggets > 0) {
        if (wallet) {
          const updated = await updateNuggetWallet(wallet.id, { balance: wallet.balance + earnedNuggets });
          setWallet(updated.data);
        } else {
          const created = await createNuggetWallet({ student_id: Number(studentId), balance: earnedNuggets });
          setWallet(created.data);
        }
      }
    } catch {
      // non-fatal: UI already updated locally
    }

    try {
      const sessionRes = await createExamSession({
        student_id: Number(studentId),
        exam_id: Number(selectedExam?.id),
        answers,
      });
      setSessionId(sessionRes.data.id);

      // Save competency breakdowns per competency
      const competencyScores: Record<string, { score: number; max: number }> = {};
      questions.forEach(q => {
        const comps = q.competency_ids ?? [];
        const isCorrect = q.correct_answer && answers[String(q.id)] === q.correct_answer;
        comps.forEach(c => {
          if (!competencyScores[c]) competencyScores[c] = { score: 0, max: 0 };
          competencyScores[c].max += 1;
          if (isCorrect) competencyScores[c].score += 1;
        });
      });

      await Promise.all(
        Object.entries(competencyScores).map(([name, { score, max }]) =>
          createCompetencyBreakdown({
            exam_session_id: sessionRes.data.id,
            competency_name: name,
            score,
            max_score: max,
            is_weak: score / max < 0.6,
          }).catch(() => null)
        )
      );
    } catch {
      // continue
    }
  };

  const progress = questions.length > 0 ? ((currentQuestionIndex + 1) / questions.length) * 100 : 0;

  if (!selectedExam) {
    return (
      <div className="page">
        <h1 style={{ marginBottom: '1rem' }}>Take an Exam</h1>
        {error && (
          <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>
            {error}
          </div>
        )}
        {loading ? (
          <p>Loading exams...</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {exams.length === 0 ? (
              <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
                <p style={{ color: 'var(--text-secondary)' }}>No exams available yet. Check back later!</p>
              </div>
            ) : (
              exams.map(exam => (
                <div key={exam.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3>{exam.title}</h3>
                    {exam.description && <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{exam.description}</p>}
                    <span className="badge" style={{ background: exam.is_active ? 'var(--accent)' : 'var(--bg-secondary)', color: exam.is_active ? '#fff' : 'var(--text-secondary)' }}>
                      {exam.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                  <button className="primary" onClick={() => handleSelectExam(exam)} disabled={!exam.is_active}>Start</button>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    );
  }

  if (showResult) {
    const correctCount = questions.filter(q => q.correct_answer && answers[String(q.id)] === q.correct_answer).length;
    const earnedNuggets = questions.reduce((sum, q) => {
      const baseReward = (q.nugget_reward_multiplier ?? 1) * 10;
      const isCorrect = q.correct_answer && answers[String(q.id)] === q.correct_answer;
      return sum + (isCorrect ? baseReward * currentMultiplier : 0);
    }, 0);

    const weakCompetencies = new Set<string>();
    const competencyScores: Record<string, { score: number; max: number }> = {};
    questions.forEach(q => {
      const comps = q.competency_ids ?? [];
      const isCorrect = q.correct_answer && answers[String(q.id)] === q.correct_answer;
      comps.forEach(c => {
        if (!competencyScores[c]) competencyScores[c] = { score: 0, max: 0 };
        competencyScores[c].max += 1;
        if (isCorrect) competencyScores[c].score += 1;
      });
    });
    Object.entries(competencyScores).forEach(([name, { score, max }]) => {
      if (score / max < 0.6) weakCompetencies.add(name);
    });

    return (
      <div className="page">
        <div className="card" style={{ textAlign: 'center', padding: '3rem', maxWidth: 600, margin: '2rem auto' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎉</div>
          <h1 style={{ marginBottom: '0.5rem' }}>Exam Complete!</h1>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            {correctCount} of {questions.length} correct
          </p>
          <div className={`badge ${animatingNugget ? 'nugget-animate' : ''}`} style={{
            background: 'var(--accent)', color: '#fff', fontSize: '1.5rem', padding: '0.75rem 1.5rem', marginBottom: '1.5rem', display: 'inline-block'
          }}>
            🪙 +{Math.round(earnedNuggets)} Nuggets
          </div>

          {/* Competency Breakdown */}
          {Object.keys(competencyScores).length > 0 && (
            <div style={{ textAlign: 'left', marginBottom: '1.5rem' }}>
              <h3 style={{ marginBottom: '0.75rem' }}>Competency Breakdown</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {Object.entries(competencyScores).map(([name, { score, max }]) => {
                  const pct = Math.round((score / max) * 100);
                  const isWeak = pct < 60;
                  return (
                    <div key={name} style={{ padding: '0.5rem 0.75rem', borderRadius: 'var(--radius-s)', background: isWeak ? '#ffe0e0' : '#e0ffe0', border: `1px solid ${isWeak ? 'var(--danger)' : '#2ecc71'}` }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                        <span style={{ fontWeight: 500 }}>{name}</span>
                        <span style={{ color: isWeak ? 'var(--danger)' : '#27ae60' }}>{pct}% {isWeak ? '⚠️ Needs work' : '✓'}</span>
                      </div>
                      {isWeak && (
                        <p style={{ fontSize: '0.8rem', color: 'var(--danger)', margin: 0 }}>
                          Review this topic before the next attempt.
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
            <button className="primary" onClick={() => navigate('/student/reviews')}>View Past Attempts</button>
            <button className="secondary" onClick={() => navigate('/student/profile')}>Back to Profile</button>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <div className="page">
      {/* Top Bar: Timer, Progress, Nuggets */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span className="badge" style={{ fontSize: '1rem', padding: '0.4rem 0.75rem', background: timer < 120 ? 'var(--danger)' : 'var(--bg-secondary)', color: timer < 120 ? '#fff' : 'var(--text)' }}>
            {timer > 0 ? `⏱ ${Math.floor(timer / 60)}:${(timer % 60).toString().padStart(2, '0')}` : '⏱ No limit'}
          </span>
          <span className="badge" style={{ fontSize: '0.9rem', background: currentMultiplier > 1 ? 'var(--accent)' : 'var(--bg-secondary)', color: currentMultiplier > 1 ? '#fff' : 'var(--text)' }}>
            🔥 {currentMultiplier}x {streak ? `(${streak.current_streak} streak)` : ''}
          </span>
          <span className={`badge ${animatingNugget ? 'nugget-animate' : ''}`} style={{ fontSize: '0.9rem', background: 'var(--accent)', color: '#fff' }}>
            🪙 {Math.round(nuggetCount)}
          </span>
        </div>
        <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Question {currentQuestionIndex + 1} of {questions.length}
        </span>
      </div>

      {/* Progress Bar */}
      <div style={{ height: 6, background: 'var(--border-light)', borderRadius: 3, overflow: 'hidden', marginBottom: '2rem' }}>
        <div style={{ height: '100%', width: `${progress}%`, background: 'var(--accent)', borderRadius: 3, transition: 'width 0.3s ease' }} />
      </div>

      {/* Question Card */}
      {currentQuestion ? (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>
              {currentQuestion.type.replace(/_/g, ' ')}
            </span>
            <span className="badge">{currentQuestion.difficulty_tier}</span>
            {currentQuestion.competency_ids?.map(cid => (
              <span key={cid} className="badge">{cid}</span>
            ))}
          </div>

          <h3 style={{ marginBottom: '1.5rem' }}>
            {currentQuestion.body || `Question ${currentQuestionIndex + 1}`}
          </h3>

          <div style={{ marginBottom: '1.5rem' }}>
            {currentQuestion.type === 'multiple_choice' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {(currentQuestion.answer_options ?? ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4']).map(opt => (
                  <label key={opt} style={{
                    display: 'flex', alignItems: 'center', gap: '0.5rem',
                    padding: '0.75rem', borderRadius: 'var(--radius-s)',
                    border: `1.5px solid ${answers[String(currentQuestion.id)] === opt ? 'var(--accent)' : 'var(--border)'}`,
                    cursor: 'pointer', background: answers[String(currentQuestion.id)] === opt ? 'rgba(0,113,227,0.08)' : 'transparent'
                  }}>
                    <input
                      type="radio"
                      name={`q-${currentQuestion.id}`}
                      value={opt}
                      checked={answers[String(currentQuestion.id)] === opt}
                      onChange={() => handleAnswer(currentQuestion.id, opt)}
                    />
                    {opt}
                  </label>
                ))}
              </div>
            )}
            {currentQuestion.type === 'code_snippet' && (
              <textarea
                value={answers[String(currentQuestion.id)] || ''}
                onChange={e => handleAnswer(currentQuestion.id, e.target.value)}
                placeholder="Write your code here..."
                rows={6}
                style={{ fontFamily: 'monospace', fontSize: '0.9rem' }}
              />
            )}
            {currentQuestion.type === 'drag_and_drop' && (
              <textarea
                value={answers[String(currentQuestion.id)] || ''}
                onChange={e => handleAnswer(currentQuestion.id, e.target.value)}
                placeholder={currentQuestion.body ? 'Arrange the items...' : 'Drag and drop items or list arranged items...'}
                rows={4}
              />
            )}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <button
              className="secondary"
              onClick={() => { if (currentQuestionIndex > 0) setCurrentQuestionIndex(prev => prev - 1); }}
              disabled={currentQuestionIndex === 0}
            >
              Previous
            </button>
            <button className="primary" onClick={handleNextQuestion}>
              {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Submit Exam'}
            </button>
          </div>
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
          <p>No questions found for this exam. Ask your instructor to add questions.</p>
          <button className="secondary" onClick={() => setSelectedExam(null)} style={{ marginTop: '1rem' }}>Back</button>
        </div>
      )}
    </div>
  );
}
