import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExams, getStudents, getEnrollments, getCompetencies, createBonusNugget } from '../api/services';
import type { ExamResponse, StudentResponse, EnrollmentResponse, CompetencyResponse } from '../types';

export default function InstructorDashboardPage() {
  const [exams, setExams] = useState<ExamResponse[]>([]);
  const [students, setStudents] = useState<StudentResponse[]>([]);
  const [enrollments, setEnrollments] = useState<EnrollmentResponse[]>([]);
  const [competencies, setCompetencies] = useState<CompetencyResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Bonus nugget grant form
  const [showGrantForm, setShowGrantForm] = useState(false);
  const [grantStudentId, setGrantStudentId] = useState<number | ''>('');
  const [grantAmount, setGrantAmount] = useState<number | ''>(10);
  const [grantJustification, setGrantJustification] = useState('');
  const [granting, setGranting] = useState(false);

  const navigate = useNavigate();
  const instructorId = Number(localStorage.getItem('instructor_id') ?? 0);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        const [examsRes, studentsRes, enrollmentsRes, competenciesRes] = await Promise.all([
          getExams(), getStudents(), getEnrollments(), getCompetencies()
        ]);
        setExams(examsRes.data);
        setStudents(studentsRes.data);
        setEnrollments(enrollmentsRes.data);
        setCompetencies(competenciesRes.data);
      } catch {
        setError('Failed to load dashboard data. Ensure backend is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleGrantNuggets = async () => {
    if (!grantStudentId || !grantAmount || !grantJustification.trim()) {
      setError('Fill in all fields for the bonus nugget grant.');
      return;
    }
    setGranting(true);
    setError('');
    try {
      await createBonusNugget({
        student_id: Number(grantStudentId),
        instructor_id: instructorId || undefined,
        amount: Number(grantAmount),
        justification: grantJustification,
      });
      setSuccess(`Granted ${grantAmount} nuggets to student #${grantStudentId}!`);
      setGrantStudentId('');
      setGrantAmount(10);
      setGrantJustification('');
      setShowGrantForm(false);
    } catch {
      setError('Failed to grant nuggets.');
    } finally {
      setGranting(false);
    }
  };

  const activeExams = exams.filter(e => e.is_active);
  const totalEnrollments = enrollments.length;

  if (loading) return <div className="page"><p>Loading dashboard...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1>Welcome, {localStorage.getItem('instructor_name') || 'Instructor'}</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Instructor Dashboard</p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="secondary" onClick={() => navigate('/instructor/heatmap')}>Competency Heatmap</button>
          <button className="primary" onClick={() => navigate('/instructor/exam-builder')}>+ Create Exam</button>
        </div>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}
      {success && <div style={{ background: '#e0ffe0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: '#27ae60', fontSize: '0.9rem' }}>{success}</div>}

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Active Exams</h3>
          <p style={{ fontSize: '2rem', fontWeight: 700 }}>{activeExams.length}</p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Total Students</h3>
          <p style={{ fontSize: '2rem', fontWeight: 700 }}>{students.length}</p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Enrollments</h3>
          <p style={{ fontSize: '2rem', fontWeight: 700 }}>{totalEnrollments}</p>
        </div>
        <div className="card">
          <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.3rem' }}>Competencies</h3>
          <p style={{ fontSize: '2rem', fontWeight: 700 }}>{competencies.length}</p>
        </div>
      </div>

      {/* Bonus Nugget Grant */}
      <section style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="section-title">Grant Bonus Nuggets</h2>
          <button className="secondary" onClick={() => setShowGrantForm(!showGrantForm)}>
            {showGrantForm ? 'Hide' : 'Grant Nuggets'}
          </button>
        </div>
        {showGrantForm && (
          <div className="card">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '0.75rem' }}>
              <div>
                <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Student</label>
                <select value={grantStudentId} onChange={e => setGrantStudentId(e.target.value === '' ? '' : Number(e.target.value))}>
                  <option value="">Select a student...</option>
                  {students.map(s => <option key={s.id} value={s.id}>{s.name} (#{s.id})</option>)}
                </select>
              </div>
              <div>
                <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Amount (nuggets)</label>
                <input type="number" value={grantAmount} onChange={e => setGrantAmount(e.target.value === '' ? '' : Number(e.target.value))} min={1} placeholder="10" />
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{ fontWeight: 500, display: 'block', marginBottom: '0.3rem', fontSize: '0.9rem' }}>Justification</label>
                <textarea value={grantJustification} onChange={e => setGrantJustification(e.target.value)} placeholder="Reason for bonus (e.g. exceptional participation)" rows={2} />
              </div>
            </div>
            <button className="primary" onClick={handleGrantNuggets} disabled={granting}>{granting ? 'Granting...' : 'Grant Nuggets'}</button>
          </div>
        )}
      </section>

      {/* Active Exams */}
      <section style={{ marginBottom: '2rem' }}>
        <h2 className="section-title">Active Exams</h2>
        {activeExams.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>No active exams yet. Create your first exam to get started!</p>
            <button className="primary" onClick={() => navigate('/instructor/exam-builder')}>Create an Exam</button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {activeExams.map(exam => (
              <div key={exam.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ marginBottom: '0.25rem' }}>{exam.title}</h3>
                  {exam.description && <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{exam.description}</p>}
                  <span className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>Active</span>
                </div>
                <button className="secondary" onClick={() => navigate(`/instructor/exam-builder?id=${exam.id}`)}>Manage</button>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Competency Coverage */}
      <section>
        <h2 className="section-title">Competency Coverage</h2>
        <div className="card">
          {competencies.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No competencies defined yet. Create competencies via the exam builder.</p>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {competencies.map(comp => (
                <span key={comp.id} className="badge" style={{ background: 'var(--accent)', color: '#fff' }}>{comp.name}</span>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
