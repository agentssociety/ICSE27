import { Link, useLocation, useNavigate } from 'react-router-dom';

export default function Layout({ children }: { children: React.ReactNode }) {
  // Re-read localStorage on every route change so nav updates after login/logout
  useLocation();
  const navigate = useNavigate();

  const studentId = localStorage.getItem('student_id');
  const studentName = localStorage.getItem('student_name');
  const instructorId = localStorage.getItem('instructor_id');
  const instructorName = localStorage.getItem('instructor_name');

  const role: 'student' | 'instructor' | 'guest' =
    instructorId ? 'instructor' : studentId ? 'student' : 'guest';

  const handleLogout = () => {
    localStorage.removeItem('student_id');
    localStorage.removeItem('student_name');
    localStorage.removeItem('instructor_id');
    localStorage.removeItem('instructor_name');
    localStorage.removeItem('leaderboard_opt_out');
    navigate('/');
  };

  return (
    <div>
      <nav>
        {/* Logo */}
        <Link to="/" style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text)', whiteSpace: 'nowrap' }}>
          🏆 Competency Platform
        </Link>

        <div style={{ flex: 1 }} />

        {/* Guest: show login/signup options */}
        {role === 'guest' && (
          <>
            <Link to="/instructor/login" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Instructor Login</Link>
            <Link to="/instructor/register" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Instructor Signup</Link>
            <Link to="/student/login" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Student Login</Link>
            <Link to="/student/register">
              <button className="primary" style={{ fontSize: '0.875rem', padding: '0.35rem 1rem' }}>Student Signup</button>
            </Link>
          </>
        )}

        {/* Student: student-only pages */}
        {role === 'student' && (
          <>
            <Link to="/student/profile" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Profile</Link>
            <Link to="/student/exam" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Take Exam</Link>
            <Link to="/student/rewards" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Rewards</Link>
            <Link to="/student/leaderboard" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Leaderboard</Link>
            <Link to="/student/reviews" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Past Reviews</Link>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginLeft: '0.5rem', paddingLeft: '0.75rem', borderLeft: '1px solid var(--border-light)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>👤 {studentName || `Student #${studentId}`}</span>
              <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.3rem 0.75rem' }} onClick={handleLogout}>Logout</button>
            </div>
          </>
        )}

        {/* Instructor: instructor-only pages */}
        {role === 'instructor' && (
          <>
            <Link to="/instructor/dashboard" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Dashboard</Link>
            <Link to="/instructor/exam-builder" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Exam Builder</Link>
            <Link to="/instructor/cohorts" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Cohorts</Link>
            <Link to="/instructor/heatmap" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Heatmap</Link>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginLeft: '0.5rem', paddingLeft: '0.75rem', borderLeft: '1px solid var(--border-light)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>🎓 {instructorName || 'Instructor'}</span>
              <button className="secondary" style={{ fontSize: '0.8rem', padding: '0.3rem 0.75rem' }} onClick={handleLogout}>Logout</button>
            </div>
          </>
        )}
      </nav>
      <main className="page">{children}</main>
    </div>
  );
}
