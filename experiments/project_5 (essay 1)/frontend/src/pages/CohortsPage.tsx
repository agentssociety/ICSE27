import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCohorts, createCohort, getStudents, getExams, createEnrollment } from '../api/services';
import type { CohortResponse, StudentResponse, ExamResponse } from '../types';

export default function CohortsPage() {
  const [cohorts, setCohorts] = useState<CohortResponse[]>([]);
  const [students, setStudents] = useState<StudentResponse[]>([]);
  const [exams, setExams] = useState<ExamResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newCohortName, setNewCohortName] = useState('');
  const [enrollStudentId, setEnrollStudentId] = useState<number | ''>('');
  const [enrollCohortId, setEnrollCohortId] = useState<number | ''>('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [cohortsRes, studentsRes, examsRes] = await Promise.all([
          getCohorts(), getStudents(), getExams()
        ]);
        setCohorts(cohortsRes.data);
        setStudents(studentsRes.data);
        setExams(examsRes.data);
      } catch {
        setError('Failed to load data.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleCreateCohort = async () => {
    if (!newCohortName.trim()) return;
    try {
      const res = await createCohort({ name: newCohortName });
      setCohorts(prev => [...prev, res.data]);
      setNewCohortName('');
    } catch {
      setError('Failed to create cohort.');
    }
  };

  const handleEnroll = async () => {
    if (enrollStudentId === '' || enrollCohortId === '') { setError('Select both a student and a cohort.'); return; }
    try {
      await createEnrollment({ student_id: Number(enrollStudentId), cohort_id: Number(enrollCohortId) });
      setEnrollStudentId('');
      setEnrollCohortId('');
    } catch {
      setError('Failed to enroll student.');
    }
  };

  if (loading) return <div className="page"><p>Loading cohorts...</p></div>;

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Cohort Management</h1>
        <button className="secondary" onClick={() => navigate('/instructor/dashboard')}>Back to Dashboard</button>
      </div>

      {error && <div style={{ background: '#ffe0e0', padding: '0.75rem', borderRadius: 'var(--radius-s)', marginBottom: '1rem', color: 'var(--danger)', fontSize: '0.9rem' }}>{error}</div>}

      {/* Create Cohort */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Create Cohort</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-end' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Cohort Name</label>
            <input
              type="text"
              value={newCohortName}
              onChange={e => setNewCohortName(e.target.value)}
              placeholder="e.g. CS101 Fall 2026"
              onKeyDown={e => e.key === 'Enter' && handleCreateCohort()}
            />
          </div>
          <button className="primary" onClick={handleCreateCohort}>Create Cohort</button>
        </div>
      </div>

      {/* Enroll Student */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 className="section-title">Enroll Student in Cohort</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 180 }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Student</label>
            <select value={enrollStudentId} onChange={e => setEnrollStudentId(e.target.value ? Number(e.target.value) : '')}>
              <option value="">Choose a student...</option>
              {students.map(s => <option key={s.id} value={s.id}>{s.name} ({s.email})</option>)}
            </select>
          </div>
          <div style={{ flex: 1, minWidth: 180 }}>
            <label style={{ display: 'block', marginBottom: '0.3rem', fontWeight: 500, fontSize: '0.9rem' }}>Cohort</label>
            <select value={enrollCohortId} onChange={e => setEnrollCohortId(e.target.value ? Number(e.target.value) : '')}>
              <option value="">Choose a cohort...</option>
              {cohorts.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          <button className="primary" onClick={handleEnroll}>Enroll</button>
        </div>
      </div>

      {/* Cohort List */}
      <section style={{ marginBottom: '2rem' }}>
        <h2 className="section-title">Cohorts ({cohorts.length})</h2>
        {cohorts.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No cohorts yet. Create one above.</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {cohorts.map(c => (
              <div key={c.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>{c.name}</strong>
                  <span className="badge" style={{ marginLeft: '0.5rem' }}>#{c.id}</span>
                </div>
                {c.instructor_id && <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Instructor #{c.instructor_id}</span>}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Exams */}
      <section>
        <h2 className="section-title">Exams</h2>
        <div className="card">
          {exams.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No exams created yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {exams.map(exam => (
                <div key={exam.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span>{exam.title}</span>
                  <span className="badge" style={{ background: exam.is_active ? 'var(--accent)' : 'var(--bg-secondary)', color: exam.is_active ? '#fff' : 'var(--text-secondary)' }}>
                    {exam.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
