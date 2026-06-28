import { Link, useLocation } from "react-router-dom";

const navLinks = [
  { path: "/", label: "Home" },
  { path: "/login", label: "Login" },
  { path: "/audit-log", label: "Audit Log" },
  { path: "/flagged-transactions", label: "Flagged" },
  { path: "/admin/accounts", label: "Admin" },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();

  return (
    <>
      <nav>
        {navLinks.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            style={{
              fontWeight: location.pathname === link.path ? 600 : 400,
              color:
                location.pathname === link.path
                  ? "var(--accent)"
                  : "var(--text-secondary)",
            }}
          >
            {link.label}
          </Link>
        ))}
      </nav>
      <main className="page">{children}</main>
    </>
  );
}
