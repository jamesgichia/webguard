import { useState, useEffect } from 'react';
import { ShieldCheck, Loader2 } from 'lucide-react';
import { api } from '../services/api';

interface Stats {
  total_scans: number;
  average_score: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [targetUrl, setTargetUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await api.get('/dashboard/stats');
      setStats(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const startScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetUrl) return;
    
    setIsScanning(true);
    try {
      await api.post('/scans/', { target_url: targetUrl, profile: 'Standard' });
      setTargetUrl('');
      // Optimistically fetch stats again
      fetchStats();
    } catch (err) {
      console.error('Failed to start scan:', err);
    } finally {
      setIsScanning(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-cyber-500" />
      </div>
    );
  }

  return (
    <>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Security Dashboard</h2>
        <p className="text-slate-500 dark:text-slate-400">Overview of your web application security posture.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-cyber-500/30 transition-colors">
          <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Total Scans</h3>
          <p className="text-3xl font-bold text-slate-900 dark:text-white">{stats?.total_scans || 0}</p>
        </div>
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-success/30 transition-colors">
          <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Average Score</h3>
          <p className="text-3xl font-bold text-success">
            {stats?.average_score ? `${stats.average_score.toFixed(1)}/100` : 'N/A'}
          </p>
        </div>
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-danger/30 transition-colors">
          <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Active Alerts</h3>
          <p className="text-3xl font-bold text-danger">0</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
          <h3 className="font-semibold text-slate-900 dark:text-white">Start New Scan</h3>
        </div>
        <div className="p-6">
          <form onSubmit={startScan} className="flex flex-col items-center justify-center py-6 text-center">
            <div className="w-16 h-16 rounded-full bg-cyber-50 dark:bg-cyber-900/30 flex items-center justify-center mb-4 text-cyber-500">
               <ShieldCheck className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">Ready to secure your application?</h3>
            <p className="text-slate-500 dark:text-slate-400 max-w-sm mb-6">
              Enter the URL of the web application you'd like to scan for OWASP Top 10 vulnerabilities.
            </p>
            
            <div className="flex w-full max-w-md space-x-2">
              <input
                type="url"
                required
                placeholder="https://example.com"
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
                className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-slate-900 dark:text-white focus:ring-2 focus:ring-cyber-500 outline-none"
              />
              <button 
                type="submit" 
                disabled={isScanning}
                className="px-5 py-2.5 bg-cyber-500 hover:bg-cyber-600 disabled:opacity-50 text-white rounded-lg font-medium transition-colors shadow-md shadow-cyber-500/20 flex items-center space-x-2"
              >
                {isScanning ? <Loader2 className="w-5 h-5 animate-spin" /> : <span>Scan</span>}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
