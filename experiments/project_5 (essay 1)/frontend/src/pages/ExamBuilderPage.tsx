import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  getExams, createExam, updateExam,
  getQuestions, createQuestion, deleteQuestion,
  getCompetencies, createCompetency,
  getSchedules, createSchedule, updateSchedule,
} from '../api/services';
import type { ExamResponse, QuestionResponse, CompetencyResponse, QuestionType, DifficultyTier, ScheduleResponse } from '../types';

export default function ExamBuilderPage() {
  const [searchParams] = useSearchParams();
  const examIdParam = searchParams.get('id');
  const navigate = useNavigate();

  const [savedExamId, setSavedExamId] = useState<number | null>(examIdParam ? Number(examIdParam) : null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [questions, setQuestions] = useState<QuestionResponse[]>([]);
  const [competencies, setCompetencies] = useState<CompetencyResponse[]>([]);
  const [schedule, setSchedule] = useState<ScheduleResponse | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [newCompetencyName, setNewCompetencyName] = useState('');

  // Scheduling form
  const [showSchedule, setShowSchedule] = useState(false);
  const [openDate, setOpenDate] = useState('');
  const [closeDate, setCloseDate] = useState('');
  const [timeLimitMinutes, setTimeLimitMinutes] = useState<number | ''>('');

  // New question form
  const [showNewQuestion, setShowNewQuestion] = useState(false);
  const [qBody, setQBody] = useState('');
  const [qType, setQType] = useState<QuestionType>('multiple_choice');
  const [qDifficulty, setQDifficulty] = useState<DifficultyTier>('beginner');
  const [qMultiplier, setQMultiplier] = useState(1);
  const [qCompetencyIds, setQCompetencyIds] = useState<number[]>([]);
  const [qAnswerOptions, setQAnswerOptions] = useState(['', '', '']);
  const [qCorrectIndex, setQCorrectIndex] = useState<number | null>(null);
  const [qCorrectAnswerText, setQCorrectAnswerText] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [examsRes, compsRes, schedulesRes] = await Promise.all([
          getExams(), getCompetencies(), getSchedules()
        ]);
        setCompetencies(compsRes.data);

        const eid = examIdParam ? Number(examIdParam) : null;
        if (eid) {
          const exam = examsRes.data.find(e => e.id === eid);
          if (exam) {
            setTitle(exam.title);
            setDescription(exam.description ?? '');
            setIsActive(exam.is_active);
          }
          const questionsRes = await getQuestions(eid);
          setQuestions(questionsRes.data);
          const examSchedule = schedulesRes.data.find(s => s.exam_id === String(eid));
          if (examSchedule) {
            setSchedule(examSchedule);
            setOpenDate(examSchedule.open_date?.slice(0, 16) ?? '');
            setCloseDate(examSchedule.close_date?.slice(0, 16) ?? '');
            setTimeLimitMinutes(examSchedule.per_attempt_time_limit_minutes ?? '');
          }
        }
      } catch {
        setError('Failed to load data from backend.');
      }
    };
    fetchData();
  }, [examIdParam]);

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      if (!savedExamId) {
        const res = await createExam({ title: title || 'Untitled Exam', description, is_active: isActive, cohort_ids: [] });
        setSavedExamId(res.data.id);
        navigate(`/instructor/exam-builder?id=${res.data.id}`, { replace: true });
      } else {
        await updateExam(String(savedExamId), { title, description, is_active: isActive });
      }
      setSuccess('Exam saved!');
    } catch {
      setError('Failed to save exam.');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveSchedule = async () => {
    if (!savedExamId) { setError('Save the exam first before scheduling.'); return; }
    setSaving(true);
    setError('');
    try {
      const payload = {
        exam_id: String(savedExamId),
        open_date: openDate,
        close_date: closeDate,
        per_attempt_time_limit_minutes: timeLimitMinutes !== '' ? Number(timeLimitMinutes) : null,
      };
      if (schedule) {
        const res = await updateSchedule(schedule.id, payload);
        setSchedule(res.data);
      } else {
        const res = await createSchedule(payload);
        setSchedule(res.data);
      }
      setSuccess('Schedule saved!');
    } catch {
      setError('Failed to save schedule.');
    } finally {
      setSaving(false);
    }
  };

  const handleAddQuestion = async () => {
    if (!savedExamId) { setError('Save the exam first before adding questions.'); return; }
    setSaving(true);
    try {
      const filledOptions = qAnswerOptions.filter(o => o.trim());
      if (qType === 'multiple_choice') {
        if (filledOptions.length < 2) { setError('Please fill in at least 2 answer options.'); setSaving(false); return; }
        if (qCorrectIndex === null || !qAnswerOptions[qCorrectIndex]?.trim()) { setError('Please mark one option as the correct answer.'); setSaving(false); return; }
      }
      const correctAnswer = qType === 'multiple_choice'
        ? qAnswerOptions[qCorrectIndex as number].trim()
        : qCorrectAnswerText.trim() || undefined;
      const res = await createQuestion({
        type: qType,
        difficulty_tier: qDifficulty,
        nugget_reward_multiplier: qMultiplier,
        body: qBody || undefined,
        answer_options: qType === 'multiple_choice' ? filledOptions : undefined,
        correct_answer: correctAnswer,
        exam_id: savedExamId,
        competency_ids: qCompetencyIds.length > 0 ? qCompetencyIds : undefined,
      });
      setQuestions(prev => [...prev, res.data]);
      setShowNewQuestion(false);
      setQBody('');
      setQType('multiple_choice');
      setQDifficulty('beginner');
      setQMultiplier(1);
      setQCompetencyIds([]);
      setQAnswerOptions(['', '', '']);
      setQCorrectIndex(null);
      setQCorrectAnswerText('');
    } catch {
      setError('Failed to create question.');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteQuestion = async (id: number) => {
    try {
      await deleteQuestion(id);
      setQuestions(prev => prev.filter(q => q.id !== id));
    } catch {
      setError('Failed to delete question.');
    }
  };

  const handleAddCompetency = async () => {
    if (!newCompetencyName.trim()) return;
    try {
      const res = await createCompetency({ name: newCompetencyName });
      setCompetencies(prev => [...prev, res.data]);
      setNewCompetencyName('');
    } catch {
      setError('Failed to create competency.');
    }
  };

  const toggleCompetency = (id: number) => {
    setQCompetencyIds(prev => prev.includes(id) ? prev.filter(c => c !== id) : [...prev, id]);
  };

  const updateAnswerOption = (index: number, value: string) => {
    setQAnswerOptions(prev => prev.map((o, i) => i === index ? value : o));
  };

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Exam Builder</h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="secondary" onClick={() => navigate('/instructor/dashboard')}>Back</button>
          <button className="primary" onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save Exam'}</button>
        </div>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}
      {success && <div style={{ background: '#e0ffe0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: '#27ae60', fontSize: '0.9rem' }}>{success}</div>}

      {/* Exam Metadata */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Exam Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.75rem' }}>
          <div>
            <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem' }}>Title</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="Exam title" />
          </div>
          <div>
            <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem' }}>Description</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Optional description" rows={2} />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input type="checkbox" id="isActive" checked={isActive} onChange={e => setIsActive(e.target.checked)} />
            <label htmlFor="isActive" style={{ fontWeight: 500 }}>Active (visible to students)</label>
          </div>
        </div>
      </div>

      {/* Scheduling */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <h3>Schedule</h3>
          <button className="secondary" onClick={() => setShowSchedule(!showSchedule)}>
            {showSchedule ? 'Hide' : schedule ? 'Edit Schedule' : 'Set Schedule'}
          </button>
        </div>
        {schedule && !showSchedule && (
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Open: {schedule.open_date?.slice(0, 16)} | Close: {schedule.close_date?.slice(0, 16)}
            {schedule.per_attempt_time_limit_minutes && ` | Time limit: ${schedule.per_attempt_time_limit_minutes} min`}
          </div>
        )}
        {!schedule && !showSchedule && (
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>No schedule set. Students can attempt anytime when the exam is active.</p>
        )}
        {showSchedule && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Open Date</label>
              <input type="datetime-local" value={openDate} onChange={e => setOpenDate(e.target.value)} />
            </div>
            <div>
              <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Close Date</label>
              <input type="datetime-local" value={closeDate} onChange={e => setCloseDate(e.target.value)} />
            </div>
            <div>
              <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Time Limit (minutes)</label>
              <input type="number" value={timeLimitMinutes} onChange={e => setTimeLimitMinutes(e.target.value === '' ? '' : Number(e.target.value))} min={5} placeholder="No limit" />
            </div>
            <div style={{ gridColumn: '1 / -1' }}>
              <button className="primary" onClick={handleSaveSchedule} disabled={saving}>Save Schedule</button>
            </div>
          </div>
        )}
      </div>

      {/* Questions */}
      <section style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="section-title">Questions ({questions.length})</h2>
          <button className="primary" onClick={() => setShowNewQuestion(true)}>+ Add Question</button>
        </div>

        {showNewQuestion && (
          <div className="card" style={{ marginBottom: '1rem' }}>
            <h3 style={{ marginBottom: '1rem' }}>New Question</h3>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Question Body</label>
              <textarea value={qBody} onChange={e => setQBody(e.target.value)} placeholder="Enter the question text..." rows={3} />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.75rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Type</label>
                <select value={qType} onChange={e => { setQType(e.target.value as QuestionType); setQCorrectIndex(null); setQCorrectAnswerText(''); }}>
                  <option value="multiple_choice">Multiple Choice</option>
                  <option value="drag_and_drop">Drag & Drop</option>
                  <option value="code_snippet">Code Snippet</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Difficulty</label>
                <select value={qDifficulty} onChange={e => setQDifficulty(e.target.value as DifficultyTier)}>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Nugget Multiplier</label>
                <input type="number" value={qMultiplier} onChange={e => setQMultiplier(Number(e.target.value))} min={0.5} max={5} step={0.5} />
              </div>
            </div>

            {qType === 'multiple_choice' && (
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <label style={{ fontWeight: 500, fontSize: '0.9rem' }}>Answer Options</label>
                  {qAnswerOptions.length < 6 && (
                    <button type="button" className="secondary" style={{ fontSize: '0.8rem', padding: '0.2rem 0.6rem' }} onClick={() => setQAnswerOptions(prev => [...prev, ''])}>
                      + Add Option
                    </button>
                  )}
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                  Type each option, then click "Mark correct" next to the right answer.
                </p>
                {qAnswerOptions.map((opt, i) => {
                  const label = String.fromCharCode(65 + i); // A, B, C, D...
                  const isCorrect = qCorrectIndex === i;
                  return (
                    <div key={i} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem', alignItems: 'center' }}>
                      <span style={{ fontWeight: 600, minWidth: '1.2rem', color: isCorrect ? '#27ae60' : 'var(--text-secondary)' }}>{label}</span>
                      <input
                        type="text"
                        value={opt}
                        onChange={e => updateAnswerOption(i, e.target.value)}
                        placeholder={`Option ${label}`}
                        style={{ flex: 1, borderColor: isCorrect ? '#27ae60' : undefined, outline: isCorrect ? '2px solid #27ae60' : undefined }}
                      />
                      <button
                        type="button"
                        onClick={() => setQCorrectIndex(isCorrect ? null : i)}
                        style={{
                          padding: '0.3rem 0.7rem', fontSize: '0.8rem', borderRadius: 'var(--radius-s)',
                          border: `1.5px solid ${isCorrect ? '#27ae60' : '#ccc'}`,
                          background: isCorrect ? '#27ae60' : 'transparent',
                          color: isCorrect ? '#fff' : 'var(--text-secondary)',
                          cursor: 'pointer', whiteSpace: 'nowrap', fontWeight: isCorrect ? 700 : 400,
                        }}
                      >
                        {isCorrect ? '✓ Correct' : 'Mark correct'}
                      </button>
                      {qAnswerOptions.length > 2 && (
                        <button type="button" onClick={() => {
                          setQAnswerOptions(prev => prev.filter((_, idx) => idx !== i));
                          if (qCorrectIndex === i) setQCorrectIndex(null);
                          else if (qCorrectIndex !== null && qCorrectIndex > i) setQCorrectIndex(qCorrectIndex - 1);
                        }} style={{ background: 'transparent', border: 'none', color: 'var(--danger)', cursor: 'pointer', fontSize: '1rem', padding: '0 0.3rem' }} title="Remove option">
                          ×
                        </button>
                      )}
                    </div>
                  );
                })}
                {qCorrectIndex !== null && qAnswerOptions[qCorrectIndex]?.trim() && (
                  <p style={{ fontSize: '0.85rem', color: '#27ae60', marginTop: '0.25rem' }}>
                    Correct answer: <strong>{qAnswerOptions[qCorrectIndex]}</strong>
                  </p>
                )}
              </div>
            )}

            {qType !== 'multiple_choice' && (
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Correct Answer</label>
                <input type="text" value={qCorrectAnswerText} onChange={e => setQCorrectAnswerText(e.target.value)} placeholder="Expected answer or code output" />
              </div>
            )}

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Competencies</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.5rem' }}>
                {competencies.map(comp => (
                  <span key={comp.id} className="badge" style={{ cursor: 'pointer', background: qCompetencyIds.includes(comp.id) ? 'var(--accent)' : 'var(--bg-secondary)', color: qCompetencyIds.includes(comp.id) ? '#fff' : 'var(--text)' }} onClick={() => toggleCompetency(comp.id)}>
                    {comp.name}
                  </span>
                ))}
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input type="text" value={newCompetencyName} onChange={e => setNewCompetencyName(e.target.value)} placeholder="New competency name" onKeyDown={e => e.key === 'Enter' && handleAddCompetency()} />
                <button className="secondary" onClick={handleAddCompetency}>Add</button>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button className="primary" onClick={handleAddQuestion} disabled={saving}>Create Question</button>
              <button className="secondary" onClick={() => setShowNewQuestion(false)}>Cancel</button>
            </div>
          </div>
        )}

        {questions.length === 0 && !showNewQuestion && (
          <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No questions yet. Click "Add Question" to start building your exam.</p>
          </div>
        )}

        {questions.map((q, i) => (
          <div key={q.id} className="card" style={{ marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '0.4rem', flexWrap: 'wrap' }}>
                  <strong>Q{i + 1}</strong>
                  <span className="badge">{q.type.replace(/_/g, ' ')}</span>
                  <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>{q.difficulty_tier}</span>
                  <span className="badge">{q.nugget_reward_multiplier ?? 1}x</span>
                  {q.competency_ids?.map(cid => <span key={cid} className="badge">{cid}</span>)}
                </div>
                {q.body && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: 0 }}>{q.body.slice(0, 80)}{q.body.length > 80 ? '…' : ''}</p>}
              </div>
              <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.25rem 0.6rem', color: 'var(--danger)' }} onClick={() => handleDeleteQuestion(q.id)}>Delete</button>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
