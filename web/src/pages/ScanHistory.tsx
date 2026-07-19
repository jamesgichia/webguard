import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  Loader2,
  ExternalLink,
  Search,
  Filter,
  ChevronRight,
} from 'lucide-react';
import { api } from '../services/api';
import type { Scan } from '../types';
import {
  gradeBgColor,
  statusColor,
  scoreColor,
  formatDate,
  timeAgo,
} from '../utils/helpers';

export default function ScanHistory() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const res = await api.get('/scans/');
      setScans(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = scans.filter((scan) => {
    const matchesSearch = scan.target_url
      .toLowerCase()
      .includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === 'all' || scan.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

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
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            Scan History
          </h2>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            {scans.length} scan{scans.length !== 1 ? 's' : ''} total
          </p>
        </div>

        <Link
          to="/"
          className="btn-primary inline-flex items-center space-x-2 text-sm w-fit"
        >
          <span>New Scan</span>
        </Link>
      </div>

      {/* Filters bar */}
      <div className="glass-card p-4 mb-6">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search by URL..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200 text-sm"
            />
          </div>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="pl-10 pr-8 py-2.5 rounded-xl border border-slate-300 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200 text-sm appearance-none cursor-pointer"
            >
              <option value="all">All Status</option>
              <option value="completed">Completed</option>
              <option value="running">Running</option>
              <option value="pending">Pending</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Scans table */}
      {filtered.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <History className="w-12 h-12 text-slate-400 dark:text-slate-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">
            {scans.length === 0 ? 'No scans yet' : 'No matching scans'}
          </h3>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            {scans.length === 0
              ? 'Start your first scan from the Dashboard.'
              : 'Try adjusting your search or filter.'}
          </p>
        </div>
      ) : (
        <div className="glass-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200 dark:border-sentinel-700/50">
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Target
                  </th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Grade
                  </th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Profile
                  </th>
                  <th className="text-left px-6 py-3.5 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3.5" />
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-sentinel-700/30">
                {filtered.map((scan) => (
                  <tr
                    key={scan.id}
                    className="hover:bg-slate-50/50 dark:hover:bg-sentinel-800/30 transition-colors group"
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-slate-900 dark:text-white truncate max-w-[250px]">
                          {scan.target_url}
                        </span>
                        <a
                          href={scan.target_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-slate-400 hover:text-cyber-500 transition-colors opacity-0 group-hover:opacity-100"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold capitalize ${statusColor(scan.status)}`}
                      >
                        {scan.status === 'running' && (
                          <Loader2 className="w-3 h-3 mr-1.5 animate-spin" />
                        )}
                        {scan.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`text-sm font-bold tabular-nums ${scoreColor(scan.overall_score)}`}
                      >
                        {scan.overall_score !== null
                          ? scan.overall_score.toFixed(1)
                          : '—'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {scan.overall_grade ? (
                        <span
                          className={`inline-flex items-center justify-center w-8 h-8 rounded-lg text-sm font-bold ${gradeBgColor(scan.overall_grade)}`}
                        >
                          {scan.overall_grade}
                        </span>
                      ) : (
                        <span className="text-slate-400">—</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-slate-600 dark:text-slate-400">
                        {scan.profile}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className="text-sm text-slate-500 dark:text-slate-400"
                        title={formatDate(scan.created_at)}
                      >
                        {timeAgo(scan.created_at)}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {scan.status === 'completed' && (
                        <Link
                          to={`/scans/${scan.id}`}
                          className="inline-flex items-center space-x-1 text-sm text-cyber-500 hover:text-cyber-400 font-medium transition-colors"
                        >
                          <span>View</span>
                          <ChevronRight className="w-4 h-4" />
                        </Link>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </>
  );
}
