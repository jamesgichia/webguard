import { useEffect, useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { Shield, LogOut, Moon, Sun } from 'lucide-react';
import Sidebar from './Sidebar';

export default function Layout() {
  const [darkMode, setDarkMode] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const isAuthenticated = !!localStorage.getItem('token');
  const isLoginPage = location.pathname === '/login';

  return (
    <div className="min-h-screen transition-colors duration-300">
      {/* Subtle background gradient overlay in dark mode */}
      <div className="fixed inset-0 -z-10 dark:bg-sentinel-950">
        <div className="absolute inset-0 dark:bg-[radial-gradient(ellipse_at_top,rgba(6,182,212,0.08),transparent_50%)]" />
        <div className="absolute inset-0 dark:bg-[radial-gradient(ellipse_at_bottom_right,rgba(139,92,246,0.06),transparent_50%)]" />
      </div>

      <header className="border-b border-slate-200 dark:border-sentinel-700/50 bg-white/80 dark:bg-sentinel-900/60 backdrop-blur-xl sticky top-0 z-20">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-9 h-9 rounded-lg bg-gradient-sentinel flex items-center justify-center shadow-cyber transition-shadow group-hover:shadow-cyber-lg">
                <Shield className="text-white w-5 h-5" />
              </div>
              <h1 className="text-xl font-bold text-gradient tracking-tight">
                WebGuard
              </h1>
            </Link>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-sentinel-800 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-cyber-500/50 text-slate-500 dark:text-slate-400 hover:text-cyber-500 dark:hover:text-cyber-400"
                aria-label="Toggle dark mode"
              >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              {isAuthenticated && (
                <button
                  onClick={handleLogout}
                  className="p-2.5 rounded-xl text-slate-500 hover:text-danger dark:text-slate-400 dark:hover:text-danger hover:bg-slate-100 dark:hover:bg-sentinel-800 transition-all duration-200"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {isAuthenticated && !isLoginPage ? (
        <div className="flex">
          <Sidebar />
          <main className="flex-1 min-w-0 px-6 lg:px-8 py-8 max-w-7xl">
            <Outlet />
          </main>
        </div>
      ) : (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Outlet />
        </main>
      )}
    </div>
  );
}
