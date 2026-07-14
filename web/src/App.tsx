import { useEffect, useState } from 'react';

function App() {
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div className="min-h-screen transition-colors duration-300">
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded bg-cyber-500 flex items-center justify-center shadow-lg shadow-cyber-500/20">
                <span className="text-white font-bold text-xl block">W</span>
              </div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyber-500 to-cyber-700 dark:from-cyber-400 dark:to-cyber-200">
                WebGuard
              </h1>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-cyber-500"
              aria-label="Toggle dark mode"
            >
              <span className="text-xl">{darkMode ? '☀️' : '🌙'}</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Security Dashboard</h2>
          <p className="text-slate-500 dark:text-slate-400">Overview of your web application security posture.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-cyber-500/30 transition-colors">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Total Scans</h3>
            <p className="text-3xl font-bold text-slate-900 dark:text-white">124</p>
          </div>
          <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-success/30 transition-colors">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Average Score</h3>
            <p className="text-3xl font-bold text-success">A</p>
          </div>
          <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 hover:border-danger/30 transition-colors">
            <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Critical Issues</h3>
            <p className="text-3xl font-bold text-danger">0</p>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">
          <div className="px-6 py-5 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 flex justify-between items-center">
            <h3 className="font-semibold text-slate-900 dark:text-white">Recent Scans</h3>
            <button className="text-sm font-medium text-cyber-500 hover:text-cyber-600 dark:hover:text-cyber-400 transition-colors">
              View All
            </button>
          </div>
          <div className="p-6">
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 rounded-full bg-cyber-50 dark:bg-cyber-900/30 flex items-center justify-center mb-4 text-cyber-500">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">Ready to secure your application?</h3>
              <p className="text-slate-500 dark:text-slate-400 max-w-sm mb-6">
                Start by initiating a new security scan against your web application to populate this dashboard.
              </p>
              <button className="px-5 py-2.5 bg-cyber-500 hover:bg-cyber-600 text-white rounded-lg font-medium transition-colors shadow-md shadow-cyber-500/20 flex items-center space-x-2">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span>New Scan</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
