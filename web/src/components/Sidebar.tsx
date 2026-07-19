import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  History,
  Key,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/scans', icon: History, label: 'Scan History' },
  { to: '/keys', icon: Key, label: 'API Keys' },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  return (
    <aside
      className={`
        ${collapsed ? 'w-[68px]' : 'w-60'}
        flex-shrink-0 border-r border-slate-200 dark:border-sentinel-700/50
        bg-white/60 dark:bg-sentinel-900/40 backdrop-blur-xl
        flex flex-col transition-all duration-300 ease-in-out
        sticky top-16 h-[calc(100vh-4rem)]
      `}
    >
      {/* Navigation links */}
      <nav className="flex-1 py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const isActive =
            item.to === '/'
              ? location.pathname === '/'
              : location.pathname.startsWith(item.to);

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
                transition-all duration-200 group relative
                ${
                  isActive
                    ? 'bg-gradient-sentinel-subtle text-cyber-500 dark:text-cyber-400 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-sentinel-800 hover:text-slate-900 dark:hover:text-slate-200'
                }
              `}
              title={collapsed ? item.label : undefined}
            >
              <item.icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'text-cyber-500' : ''}`} />
              {!collapsed && <span>{item.label}</span>}

              {/* Active indicator bar */}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 rounded-r-full bg-cyber-500" />
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Collapse toggle */}
      <div className="p-3 border-t border-slate-200 dark:border-sentinel-700/50">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center p-2 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-sentinel-800 transition-all duration-200"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  );
}
