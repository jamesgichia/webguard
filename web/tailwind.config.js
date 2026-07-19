/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Midnight Sentinel — Deep dark surfaces
        sentinel: {
          950: '#0a0e1a',  // Page background (obsidian)
          900: '#111827',  // Card/panel surface
          850: '#162032',  // Elevated surface
          800: '#1e293b',  // Modals, dropdowns
          700: '#1e3a5f',  // Subtle borders
          600: '#334155',  // Muted elements
        },
        // Primary accent — Electric Cyan
        cyber: {
          50:  '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
          950: '#083344',
        },
        // Secondary accent — Vivid Violet
        violet: {
          50:  '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        // Semantic — Severity scale
        success: '#10b981',
        warning: '#f59e0b',
        danger:  '#f43f5e',
        info:    '#38bdf8',
        // Extra severity
        high:    '#f97316',
      },
      backgroundImage: {
        'gradient-sentinel': 'linear-gradient(135deg, #06b6d4, #8b5cf6)',
        'gradient-sentinel-subtle': 'linear-gradient(135deg, rgba(6,182,212,0.15), rgba(139,92,246,0.15))',
      },
      boxShadow: {
        'cyber': '0 4px 14px 0 rgba(6, 182, 212, 0.25)',
        'cyber-lg': '0 8px 25px 0 rgba(6, 182, 212, 0.3)',
        'violet': '0 4px 14px 0 rgba(139, 92, 246, 0.25)',
        'glow-cyber': '0 0 20px rgba(6, 182, 212, 0.15)',
        'glow-violet': '0 0 20px rgba(139, 92, 246, 0.15)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
    },
  },
  plugins: [],
}
