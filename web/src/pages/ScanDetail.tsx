import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Loader2,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Info,
  ExternalLink,
  Download,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import { api } from '../services/api';
import type { ScanDetail, Finding } from '../types';
import {
  gradeColor,
  gradeBgColor,
  severityColor,
  scoreColor,
  scorePercent,
  formatDate,
} from '../utils/helpers';

export default function ScanDetailPage() {
  const { scanId } = useParams<{ scanId: string }>();
  const [scan, setScan] = useState<ScanDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedFinding, setExpandedFinding] = useState<string | null>(null);
  const [downloadingJson, setDownloadingJson] = useState(false);

  useEffect(() => {
    if (scanId) fetchScanDetail();
  }, [scanId]);

  const fetchScanDetail = async () => {
    try {
      const res = await api.get(`/scans/${scanId}/detail`);
      setScan(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const downloadJson = async () => {
    if (!scanId) return;
    setDownloadingJson(true);
    try {
      const res = await api.get(`/reports/${scanId}/download/json`);
      const blob = new Blob([JSON.stringify(res.data, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `webguard-report-${scanId.slice(0, 8)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to download report:', err);
    } finally {
      setDownloadingJson(false);
    }
  };

  const toggleFinding = (id: string) => {
    setExpandedFinding(expandedFinding === id ? null : id);
  };

  const severityIcon = (severity: string) => {
    switch (severity) {
      case 'CRITICAL':
      case 'HIGH':
        return <ShieldAlert className="w-5 h-5" />;
      case 'MEDIUM':
        return <AlertTriangle className="w-5 h-5" />;
      case 'LOW':
        return <Info className="w-5 h-5" />;
      default:
        return <Info className="w-5 h-5" />;
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="relative">
          <Loader2 className="w-10 h-10 animate-spin text-cyber-500" />
          <div className="absolute inset-0 w-10 h-10 rounded-full bg-cyber-500/20 animate-ping" />
        </div>
      </div>
    );
  }

  if (!scan) {
    return (
      <div className="glass-card p-12 text-center">
        <XCircle className="w-12 h-12 text-danger mx-auto mb-4" />
        <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">
          Scan Not Found
        </h3>
        <Link to="/scans" className="text-cyber-500 hover:text-cyber-400 text-sm font-medium">
          ← Back to Scan History
        </Link>
      </div>
    );
  }

  const failedFindings = scan.findings.filter((f) => !f.passed);
  const passedFindings = scan.findings.filter((f) => f.passed);

  // Sort failed findings by severity priority
  const severityOrder: Record<string, number> = {
    CRITICAL: 0,
    HIGH: 1,
    MEDIUM: 2,
    LOW: 3,
    INFO: 4,
  };
  failedFindings.sort(
    (a, b) => (severityOrder[a.severity] ?? 5) - (severityOrder[b.severity] ?? 5)
  );

  return (
    <>
      {/* Back navigation */}
      <Link
        to="/scans"
        className="inline-flex items-center space-x-2 text-sm text-slate-500 dark:text-slate-400 hover:text-cyber-500 dark:hover:text-cyber-400 transition-colors mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Scan History</span>
      </Link>

      {/* Header card */}
      <div className="glass-card p-6 mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-3 mb-2">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white truncate">
                {scan.target_url}
              </h2>
              <a
                href={scan.target_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-cyber-500 transition-colors flex-shrink-0"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
            <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500 dark:text-slate-400">
              <span>Profile: <strong className="text-slate-700 dark:text-slate-300">{scan.profile}</strong></span>
              <span className="text-slate-300 dark:text-sentinel-700">|</span>
              <span>{formatDate(scan.completed_at || scan.created_at)}</span>
            </div>
          </div>

          {/* Score + grade */}
          <div className="flex items-center gap-6">
            <div className="text-center">
              <p className="text-xs text-slate-500 dark:text-slate-400 mb-1 uppercase tracking-wider font-medium">Score</p>
              <p className={`text-3xl font-bold tabular-nums ${scoreColor(scan.overall_score)}`}>
                {scan.overall_score !== null ? scan.overall_score.toFixed(1) : '—'}
              </p>
            </div>
            <div className="text-center">
              <p className="text-xs text-slate-500 dark:text-slate-400 mb-1 uppercase tracking-wider font-medium">Grade</p>
              <span className={`inline-flex items-center justify-center w-12 h-12 rounded-xl text-xl font-bold ${gradeBgColor(scan.overall_grade)}`}>
                {scan.overall_grade || '—'}
              </span>
            </div>
            <button
              onClick={downloadJson}
              disabled={downloadingJson}
              className="btn-primary flex items-center space-x-2 text-sm"
              title="Download JSON Report"
            >
              {downloadingJson ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              <span>JSON</span>
            </button>
          </div>
        </div>
      </div>

      {/* Dimension scores */}
      {scan.dimension_scores.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
            Security Dimensions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {scan.dimension_scores.map((dim) => (
              <div key={dim.id} className="glass-card p-5 gradient-border transition-all duration-300 hover:shadow-glow-cyber">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">
                    {dim.dimension}
                  </h4>
                  <span className={`inline-flex items-center justify-center w-7 h-7 rounded-lg text-xs font-bold ${gradeBgColor(dim.grade)}`}>
                    {dim.grade}
                  </span>
                </div>
                <div className="flex items-end justify-between mb-2">
                  <span className={`text-2xl font-bold tabular-nums ${gradeColor(dim.grade)}`}>
                    {dim.score.toFixed(1)}
                  </span>
                  <span className="text-xs text-slate-400">/10.0</span>
                </div>
                {/* Progress bar */}
                <div className="w-full h-1.5 bg-slate-200 dark:bg-sentinel-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ease-out ${
                      dim.grade === 'A' || dim.grade === 'B'
                        ? 'bg-success'
                        : dim.grade === 'C'
                        ? 'bg-warning'
                        : 'bg-danger'
                    }`}
                    style={{ width: `${scorePercent(dim.score)}%` }}
                  />
                </div>
                <div className="flex justify-between mt-1.5">
                  <span className="text-xs text-slate-400">{dim.label}</span>
                  <span className="text-xs text-slate-400">Weight: {(dim.weight * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary counts */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="glass-card p-4 text-center">
          <p className="text-2xl font-bold text-slate-900 dark:text-white">{scan.findings.length}</p>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Total Checks</p>
        </div>
        <div className="glass-card p-4 text-center">
          <p className="text-2xl font-bold text-success">{passedFindings.length}</p>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Passed</p>
        </div>
        <div className="glass-card p-4 text-center">
          <p className="text-2xl font-bold text-danger">{failedFindings.length}</p>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Issues Found</p>
        </div>
        <div className="glass-card p-4 text-center">
          <p className="text-2xl font-bold text-high">
            {failedFindings.filter((f) => f.severity === 'CRITICAL' || f.severity === 'HIGH').length}
          </p>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Critical / High</p>
        </div>
      </div>

      {/* Findings — Issues */}
      {failedFindings.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-danger" />
            <span>Issues Found ({failedFindings.length})</span>
          </h3>
          <div className="space-y-3">
            {failedFindings.map((finding) => (
              <FindingCard
                key={finding.id}
                finding={finding}
                isExpanded={expandedFinding === finding.id}
                onToggle={() => toggleFinding(finding.id)}
                severityIcon={severityIcon}
              />
            ))}
          </div>
        </div>
      )}

      {/* Findings — Passed */}
      {passedFindings.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-success" />
            <span>Passed Checks ({passedFindings.length})</span>
          </h3>
          <div className="space-y-3">
            {passedFindings.map((finding) => (
              <FindingCard
                key={finding.id}
                finding={finding}
                isExpanded={expandedFinding === finding.id}
                onToggle={() => toggleFinding(finding.id)}
                severityIcon={severityIcon}
              />
            ))}
          </div>
        </div>
      )}
    </>
  );
}

/* --------------------------------------------------------------------- */
/* Finding Card sub-component                                            */
/* --------------------------------------------------------------------- */

interface FindingCardProps {
  finding: Finding;
  isExpanded: boolean;
  onToggle: () => void;
  severityIcon: (s: string) => React.ReactNode;
}

function FindingCard({ finding, isExpanded, onToggle, severityIcon }: FindingCardProps) {
  return (
    <div className="glass-card overflow-hidden transition-all duration-300">
      {/* Clickable header row */}
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-slate-50/50 dark:hover:bg-sentinel-800/20 transition-colors"
      >
        <div className="flex items-center space-x-4 min-w-0">
          <div className={`flex-shrink-0 ${finding.passed ? 'text-success' : severityColor(finding.severity).split(' ')[1]}`}>
            {finding.passed ? <CheckCircle2 className="w-5 h-5" /> : severityIcon(finding.severity)}
          </div>
          <div className="min-w-0">
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white truncate">
              {finding.title}
            </h4>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-xs text-slate-500 dark:text-slate-400">
                {finding.owasp_id} — {finding.owasp_name}
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-3 flex-shrink-0">
          {!finding.passed && (
            <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold border ${severityColor(finding.severity)}`}>
              {finding.severity}
            </span>
          )}
          <span className="text-xs text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-sentinel-800 px-2 py-1 rounded-md">
            {finding.dimension}
          </span>
          {isExpanded ? (
            <ChevronUp className="w-4 h-4 text-slate-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-slate-400" />
          )}
        </div>
      </button>

      {/* Expanded detail panel */}
      {isExpanded && (
        <div className="px-5 pb-5 pt-1 border-t border-slate-200 dark:border-sentinel-700/30">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div>
              <h5 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
                Description
              </h5>
              <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                {finding.description}
              </p>
            </div>
            <div>
              <h5 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
                Business Impact
              </h5>
              <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                {finding.business_impact}
              </p>
            </div>
          </div>

          <div className="mt-4">
            <h5 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
              Recommendation
            </h5>
            <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
              {finding.recommendation}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 mt-4 pt-4 border-t border-slate-200 dark:border-sentinel-700/30">
            <span className="text-xs text-slate-500 dark:text-slate-400">
              Effort: <strong className="text-slate-700 dark:text-slate-300">{finding.effort}</strong>
            </span>
            {finding.references.length > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 dark:text-slate-400">References:</span>
                {finding.references.map((ref, i) => (
                  <a
                    key={i}
                    href={ref}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-cyber-500 hover:text-cyber-400 underline transition-colors"
                  >
                    [{i + 1}]
                  </a>
                ))}
              </div>
            )}
          </div>

          {/* Evidence */}
          {Object.keys(finding.evidence).length > 0 && (
            <div className="mt-4">
              <h5 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
                Evidence
              </h5>
              <pre className="text-xs bg-slate-100 dark:bg-sentinel-950 border border-slate-200 dark:border-sentinel-700/50 rounded-xl p-4 overflow-x-auto text-slate-700 dark:text-slate-300">
                {JSON.stringify(finding.evidence, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
