import { Link, useLocation } from 'react-router-dom';

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/register', label: 'Register Patient' },
    { to: '/queue', label: 'Queue' },
    { to: '/dashboard', label: 'Dashboard' },
  ];

  return (
    <>
      <nav>
        {navLinks.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            style={{
              color: location.pathname === link.to ? 'var(--accent)' : 'var(--text)',
              fontWeight: location.pathname === link.to ? 600 : 400,
            }}
          >
            {link.label}
          </Link>
        ))}
      </nav>
      <main>{children}</main>
    </>
  );
}
