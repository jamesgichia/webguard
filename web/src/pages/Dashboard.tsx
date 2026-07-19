import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  Loader2,
  Activity,
  BarChart3,
  AlertTriangle,
  ChevronRight,
  Globe,
} from 'lucide-react';
import { api } from '../services/api';
import type { DashboardStats, Scan } from '../types';
import {
  gradeBgColor,
  statusColor,
  scoreColor,
  timeAgo,
} from '../utils/helpers';

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentScans, setRecentScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [targetUrl, setTargetUrl] = useState('');
  const [profile, setProfile] = useState('Standard');
  const [isScanning, setIsScanning] = useState(false);
  const [scanError, setScanError] = useState('');

  useEffect(() => {
    Promise.all([fetchStats(), fetchRecentScans()]).finally(() =>
      setLoading(false)
    );
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/dashboard/stats');
      setStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchRecentScans = async () => {
    try {
      const res = await api.get('/scans/');
      setRecentScans(res.data.slice(0, 5));
    } catch (err) {
      console.error(err);
    }
  };

  const startScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetUrl) return;
    setScanError('');
    setIsScanning(true);
    try {
      await api.post('/scans/', { target_url: targetUrl, profile });
      setTargetUrl('');
      await Promise.all([fetchStats(), fetchRecentScans()]);
    } catch (err: any) {
      setScanError(
        err.response?.data?.detail || 'Failed to start scan. Check the URL and try again.'
      );
    } finally {
      setIsScanning(false);
    }
  };

  const scoreColorValue = (score: number | null) => scoreColor(score);

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

  return (
    <>
      {/* Page header */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
          Security Dashboard
        </h2>
        <p className="text-slate-500 dark:text-slate-400 mt-1">
          Overview of your web application security posture.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        <div className="glass-card gradient-border p-6 group transition-all duration-300 hover:shadow-glow-cyber">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">
              Total Scans
            </h3>
            <div className="w-9 h-9 rounded-lg bg-cyber-500/10 dark:bg-cyber-500/15 flex items-center justify-center text-cyber-500 group-hover:scale-110 transition-transform duration-300">
              <Activity className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">
            {stats?.total_scans ?? 0}
          </p>
          <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">
            Completed analyses
          </p>
        </div>

        <div className="glass-card gradient-border p-6 group transition-all duration-300 hover:shadow-glow-cyber">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">
              Average Score
            </h3>
            <div className="w-9 h-9 rounded-lg bg-success/10 dark:bg-success/15 flex items-center justify-center text-success group-hover:scale-110 transition-transform duration-300">
              <BarChart3 className="w-5 h-5" />
            </div>
          </div>
          <p
            className={`text-3xl font-bold tracking-tight ${
              stats?.average_score
                ? scoreColorValue(stats.average_score)
                : 'text-slate-400 dark:text-slate-500'
            }`}
          >
            {stats?.average_score
              ? `${stats.average_score.toFixed(1)}/100`
              : 'N/A'}
          </p>
          <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">
            Across all scans
          </p>
        </div>

        <div className="glass-card gradient-border p-6 group transition-all duration-300 hover:shadow-glow-violet">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">
              Active Alerts
            </h3>
            <div className="w-9 h-9 rounded-lg bg-danger/10 dark:bg-danger/15 flex items-center justify-center text-danger group-hover:scale-110 transition-transform duration-300">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-bold text-danger tracking-tight">0</p>
          <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">
            Unresolved findings
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* New Scan card */}
        <div className="glass-card overflow-hidden xl:col-span-3">
          <div className="px-6 py-4 border-b border-slate-200 dark:border-sentinel-700/50 bg-slate-50/50 dark:bg-sentinel-900/40">
            <h3 className="font-semibold text-slate-900 dark:text-white">
              Start New Scan
            </h3>
          </div>
          <div className="p-8">
            <form
              onSubmit={startScan}
              className="flex flex-col items-center justify-center py-4 text-center"
            >
              {/* Animated shield */}
              <div className="relative mb-6">
                <div className="w-20 h-20 rounded-2xl bg-gradient-sentinel-subtle flex items-center justify-center text-cyber-500 animate-float">
                  <ShieldCheck className="w-10 h-10" />
                </div>
                <div className="absolute -inset-1 rounded-2xl bg-gradient-sentinel opacity-20 blur-xl -z-10" />
              </div>

              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Ready to secure your application?
              </h3>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mb-8 text-sm leading-relaxed">
                Enter a URL to passively scan for OWASP Top 10 vulnerabilities
                — no injection, no probing, just intelligence.
              </p>

              {scanError && (
                <div className="w-full max-w-lg mb-4 p-3 bg-danger/10 border border-danger/20 text-danger rounded-xl text-sm text-left">
                  {scanError}
                </div>
              )}

              <div className="flex w-full max-w-lg flex-col sm:flex-row gap-3">
                <div className="relative flex-1">
                  <Globe className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="url"
                    required
                    placeholder="https://example.com"
                    value={targetUrl}
                    onChange={(e) => setTargetUrl(e.target.value)}
                    className="w-full rounded-xl border border-slate-300 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 pl-10 pr-4 py-3 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200"
                  />
                </div>
                <select
                  value={profile}
                  onChange={(e) => setProfile(e.target.value)}
                  className="rounded-xl border border-slate-300 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 px-4 py-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200 text-sm cursor-pointer"
                >
                  <option value="Quick">Quick</option>
                  <option value="Standard">Standard</option>
                  <option value="Deep">Deep</option>
                </select>
                <button
                  type="submit"
                  disabled={isScanning}
                  className="btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:hover:scale-100"
                >
                  {isScanning ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <span>Scan</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Recent scans */}
        <div className="glass-card overflow-hidden xl:col-span-2">
          <div className="px-5 py-4 border-b border-slate-200 dark:border-sentinel-700/50 flex items-center justify-between">
            <h3 className="font-semibold text-slate-900 dark:text-white">
              Recent Scans
            </h3>
            <Link
              to="/scans"
              className="text-xs text-cyber-500 hover:text-cyber-400 font-medium transition-colors flex items-center space-x-1"
            >
              <span>View all</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          {recentScans.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-sm text-slate-500 dark:text-slate-400">
                No scans yet. Start your first scan!
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-sentinel-700/30">
              {recentScans.map((scan) => (
                <div
                  key={scan.id}
                  className="px-5 py-3.5 hover:bg-slate-50/50 dark:hover:bg-sentinel-800/20 transition-colors"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                        {scan.target_url.replace(/^https?:\/\//, '')}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium capitalize ${statusColor(scan.status)}`}
                        >
                          {scan.status === 'running' && (
                            <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                          )}
                          {scan.status}
                        </span>
                        <span className="text-xs text-slate-400 dark:text-slate-500">
                          {timeAgo(scan.created_at)}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      {scan.overall_grade && (
                        <span
                          className={`inline-flex items-center justify-center w-7 h-7 rounded-lg text-xs font-bold ${gradeBgColor(scan.overall_grade)}`}
                        >
                          {scan.overall_grade}
                        </span>
                      )}
                      {scan.status === 'completed' && (
                        <Link
                          to={`/scans/${scan.id}`}
                          className="text-slate-400 hover:text-cyber-500 transition-colors"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
