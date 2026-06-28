interface UrgencyBadgeProps {
  level: number;
}

const urgencyLabels: Record<number, { label: string; color: string }> = {
  1: { label: 'Critical', color: 'var(--danger)' },
  2: { label: 'High', color: 'var(--warning)' },
  3: { label: 'Medium', color: 'var(--accent)' },
  4: { label: 'Low', color: 'var(--text-secondary)' },
  5: { label: 'Routine', color: 'var(--text-tertiary)' },
};

export default function UrgencyBadge({ level }: UrgencyBadgeProps) {
  const info = urgencyLabels[level] ?? { label: 'Unknown', color: 'var(--text-tertiary)' };
  return (
    <span
      className="badge"
      style={{
        background: `${info.color}20`,
        color: info.color,
        fontWeight: 600,
        fontSize: '0.75rem',
        padding: '0.125rem 0.5rem',
        borderRadius: 100,
      }}
    >
      {info.label}
    </span>
  );
}
