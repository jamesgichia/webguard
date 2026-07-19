/**
 * Shared utility functions and constants.
 */

/**
 * Returns a Tailwind color class based on the security grade.
 */
export function gradeColor(grade: string | null): string {
  switch (grade) {
    case 'A': return 'text-success';
    case 'B': return 'text-emerald-400';
    case 'C': return 'text-warning';
    case 'D': return 'text-high';
    case 'F': return 'text-danger';
    default: return 'text-slate-400';
  }
}

/**
 * Returns a Tailwind color class for the grade background badge.
 */
export function gradeBgColor(grade: string | null): string {
  switch (grade) {
    case 'A': return 'bg-success/15 text-success';
    case 'B': return 'bg-emerald-400/15 text-emerald-400';
    case 'C': return 'bg-warning/15 text-warning';
    case 'D': return 'bg-high/15 text-high';
    case 'F': return 'bg-danger/15 text-danger';
    default: return 'bg-slate-500/15 text-slate-400';
  }
}

/**
 * Returns a Tailwind color class for severity badges.
 */
export function severityColor(severity: string): string {
  switch (severity) {
    case 'CRITICAL': return 'bg-danger/15 text-danger border-danger/30';
    case 'HIGH': return 'bg-high/15 text-high border-high/30';
    case 'MEDIUM': return 'bg-warning/15 text-warning border-warning/30';
    case 'LOW': return 'bg-info/15 text-info border-info/30';
    case 'INFO': return 'bg-slate-500/15 text-slate-400 border-slate-500/30';
    default: return 'bg-slate-500/15 text-slate-400 border-slate-500/30';
  }
}

/**
 * Returns a Tailwind color class for scan status badges.
 */
export function statusColor(status: string): string {
  switch (status) {
    case 'completed': return 'bg-success/15 text-success';
    case 'running': return 'bg-cyber-500/15 text-cyber-400';
    case 'pending': return 'bg-warning/15 text-warning';
    case 'failed': return 'bg-danger/15 text-danger';
    default: return 'bg-slate-500/15 text-slate-400';
  }
}

/**
 * Returns the score as a color class (green/yellow/orange/red).
 */
export function scoreColor(score: number | null): string {
  if (score === null) return 'text-slate-400';
  if (score >= 80) return 'text-success';
  if (score >= 50) return 'text-warning';
  if (score >= 30) return 'text-high';
  return 'text-danger';
}

/**
 * Formats a dimension score (0–10) as a percentage bar width.
 */
export function scorePercent(score: number): number {
  return Math.max(0, Math.min(100, (score / 10) * 100));
}

/**
 * Formats an ISO date string to a human-readable format.
 */
export function formatDate(iso: string | null): string {
  if (!iso) return '—';
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Formats a relative time string (e.g., "2 minutes ago").
 */
export function timeAgo(iso: string | null): string {
  if (!iso) return '—';
  const now = Date.now();
  const then = new Date(iso).getTime();
  const seconds = Math.floor((now - then) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
  return formatDate(iso);
}
