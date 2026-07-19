import { useState } from 'react';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';
import { api } from '../services/api';
import {
  Shield,
  Loader2,
  Mail,
  Lock,
  Eye,
  EyeOff,
  User,
  CheckCircle2,
  XCircle,
  AlertCircle,
} from 'lucide-react';

// -----------------------------------------------------------------
// Password strength calculator
// -----------------------------------------------------------------
interface PasswordStrength {
  score: number; // 0-4
  label: string;
  color: string;
}

function getPasswordStrength(password: string): PasswordStrength {
  if (!password) return { score: 0, label: '', color: '' };
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  score = Math.min(score, 4);

  const levels: PasswordStrength[] = [
    { score: 0, label: '', color: '' },
    { score: 1, label: 'Weak', color: 'bg-danger' },
    { score: 2, label: 'Fair', color: 'bg-warning' },
    { score: 3, label: 'Good', color: 'bg-info' },
    { score: 4, label: 'Strong', color: 'bg-success' },
  ];
  return levels[score];
}

// -----------------------------------------------------------------
// Social provider config
// -----------------------------------------------------------------
const SOCIAL_PROVIDERS = [
  {
    id: 'google',
    label: 'Google',
    bg: 'hover:bg-[#4285F4]/10 border-[#4285F4]/30 hover:border-[#4285F4]',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
      </svg>
    ),
  },
  {
    id: 'microsoft',
    label: 'Microsoft',
    bg: 'hover:bg-[#00A4EF]/10 border-[#00A4EF]/30 hover:border-[#00A4EF]',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
        <path d="M11.5 3H3v8.5h8.5V3z" fill="#F25022"/>
        <path d="M21 3h-8.5v8.5H21V3z" fill="#7FBA00"/>
        <path d="M11.5 12.5H3V21h8.5v-8.5z" fill="#00A4EF"/>
        <path d="M21 12.5h-8.5V21H21v-8.5z" fill="#FFB900"/>
      </svg>
    ),
  },
  {
    id: 'github',
    label: 'GitHub',
    bg: 'hover:bg-slate-500/10 border-slate-400/30 hover:border-slate-400',
    icon: (
      <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 text-slate-700 dark:text-slate-300">
        <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
      </svg>
    ),
  },
];

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [loading, setLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  // If already authenticated, redirect away
  if (localStorage.getItem('token')) {
    return <Navigate to={(location.state as any)?.from?.pathname || '/'} replace />;
  }

  const strength = getPasswordStrength(password);
  const passwordsMatch = confirmPassword === '' || password === confirmPassword;
  const confirmTouched = confirmPassword.length > 0;

  const switchMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setSuccess('');
    setPassword('');
    setConfirmPassword('');
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Client-side validation for registration
    if (isRegistering) {
      if (password !== confirmPassword) {
        setError('Passwords do not match.');
        return;
      }
      if (password.length < 8) {
        setError('Password must be at least 8 characters.');
        return;
      }
    }

    setLoading(true);
    try {
      if (isRegistering) {
        await api.post('/auth/register', { email, password });
      }

      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await api.post('/auth/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      localStorage.setItem('token', res.data.access_token);
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSocialLogin = (providerId: string) => {
    setSocialLoading(providerId);
    // Redirect to the backend OAuth flow
    const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const returnUrl = encodeURIComponent(window.location.origin + '/auth/callback');
    window.location.href = `${apiBase}/api/v1/auth/oauth/${providerId}?redirect_uri=${returnUrl}`;
  };

  const inputBase =
    'w-full rounded-xl border bg-white dark:bg-sentinel-850 py-2.5 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200 text-sm';

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="glass-card gradient-border p-8 shadow-2xl transition-all duration-300">

          {/* Logo & heading */}
          <div className="flex flex-col items-center justify-center mb-7">
            <div className="relative mb-4">
              <div className="w-14 h-14 rounded-2xl bg-gradient-sentinel flex items-center justify-center shadow-cyber">
                <Shield className="text-white w-8 h-8" />
              </div>
              <div className="absolute -inset-2 rounded-2xl bg-gradient-sentinel opacity-20 blur-xl -z-10" />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
              {isRegistering ? 'Create Account' : 'Welcome Back'}
            </h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
              {isRegistering
                ? 'Start securing your applications today'
                : 'Sign in to your WebGuard dashboard'}
            </p>
          </div>

          {/* Social login buttons */}
          <div className="space-y-2.5 mb-6">
            <div className="grid grid-cols-3 gap-2.5">
              {SOCIAL_PROVIDERS.map((provider) => (
                <button
                  key={provider.id}
                  type="button"
                  disabled={!!socialLoading}
                  onClick={() => handleSocialLogin(provider.id)}
                  className={`
                    flex items-center justify-center gap-2 rounded-xl border py-2.5 px-3
                    bg-white dark:bg-sentinel-850 transition-all duration-200
                    disabled:opacity-50 disabled:cursor-not-allowed
                    ${provider.bg}
                  `}
                  title={`Continue with ${provider.label}`}
                >
                  {socialLoading === provider.id ? (
                    <Loader2 className="w-4 h-4 animate-spin text-slate-400" />
                  ) : (
                    provider.icon
                  )}
                  <span className="text-xs font-medium text-slate-700 dark:text-slate-300 hidden sm:inline">
                    {provider.label}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="flex items-center gap-4 mb-6">
            <div className="flex-1 h-px bg-slate-200 dark:bg-sentinel-700/60" />
            <span className="text-xs text-slate-400 dark:text-slate-500 font-medium">
              or continue with email
            </span>
            <div className="flex-1 h-px bg-slate-200 dark:bg-sentinel-700/60" />
          </div>

          {/* Error / Success banners */}
          {error && (
            <div className="mb-5 p-3.5 bg-danger/10 border border-danger/20 text-danger rounded-xl text-sm font-medium flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
          {success && (
            <div className="mb-5 p-3.5 bg-success/10 border border-success/20 text-success rounded-xl text-sm font-medium flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>{success}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4" noValidate>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                Email address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-slate-500 pointer-events-none" />
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  className={`${inputBase} pl-10 pr-4 border-slate-300 dark:border-sentinel-700`}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                  Password
                </label>
                {!isRegistering && (
                  <button
                    type="button"
                    className="text-xs text-cyber-500 hover:text-cyber-400 font-medium transition-colors"
                  >
                    Forgot password?
                  </button>
                )}
              </div>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-slate-500 pointer-events-none" />
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  autoComplete={isRegistering ? 'new-password' : 'current-password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className={`${inputBase} pl-10 pr-11 border-slate-300 dark:border-sentinel-700`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {/* Password strength meter — only when registering */}
              {isRegistering && password.length > 0 && (
                <div className="mt-2">
                  <div className="flex gap-1 mb-1">
                    {[1, 2, 3, 4].map((level) => (
                      <div
                        key={level}
                        className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                          strength.score >= level
                            ? strength.color
                            : 'bg-slate-200 dark:bg-sentinel-700'
                        }`}
                      />
                    ))}
                  </div>
                  {strength.label && (
                    <p className={`text-xs font-medium ${
                      strength.score === 4 ? 'text-success' :
                      strength.score === 3 ? 'text-info' :
                      strength.score === 2 ? 'text-warning' : 'text-danger'
                    }`}>
                      {strength.label} password
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Confirm password — only when registering */}
            {isRegistering && (
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                  Confirm password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-slate-500 pointer-events-none" />
                  <input
                    id="confirm-password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    required
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    className={`${inputBase} pl-10 pr-11 transition-all ${
                      confirmTouched && !passwordsMatch
                        ? 'border-danger dark:border-danger focus:ring-danger/50 focus:border-danger'
                        : confirmTouched && passwordsMatch
                        ? 'border-success dark:border-success focus:ring-success/50 focus:border-success'
                        : 'border-slate-300 dark:border-sentinel-700'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                  >
                    {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                  {/* Match indicator icon */}
                  {confirmTouched && (
                    <div className="absolute right-10 top-1/2 -translate-y-1/2">
                      {passwordsMatch ? (
                        <CheckCircle2 className="w-4 h-4 text-success" />
                      ) : (
                        <XCircle className="w-4 h-4 text-danger" />
                      )}
                    </div>
                  )}
                </div>
                {confirmTouched && !passwordsMatch && (
                  <p className="mt-1 text-xs text-danger">Passwords do not match</p>
                )}
              </div>
            )}

            {/* Terms checkbox — only for registration */}
            {isRegistering && (
              <div className="flex items-start space-x-2.5">
                <input
                  id="terms"
                  type="checkbox"
                  required
                  className="mt-0.5 w-4 h-4 rounded border-slate-300 dark:border-sentinel-700 accent-cyber-500 cursor-pointer"
                />
                <label htmlFor="terms" className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed cursor-pointer">
                  I agree to the{' '}
                  <a href="#" className="text-cyber-500 hover:text-cyber-400 underline">Terms of Service</a>
                  {' '}and{' '}
                  <a href="#" className="text-cyber-500 hover:text-cyber-400 underline">Privacy Policy</a>
                </label>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading || (isRegistering && confirmTouched && !passwordsMatch)}
              className="btn-primary w-full flex justify-center items-center py-3 mt-2 disabled:opacity-50 disabled:hover:scale-100 font-semibold"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : isRegistering ? (
                <>
                  <User className="w-4 h-4 mr-2" />
                  Create Account
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Toggle mode */}
          <p className="mt-5 text-center text-sm text-slate-500 dark:text-slate-400">
            {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
            <button
              onClick={switchMode}
              className="text-cyber-500 hover:text-cyber-400 font-semibold transition-colors duration-200"
            >
              {isRegistering ? 'Sign in' : 'Sign up for free'}
            </button>
          </p>
        </div>

        {/* Footer note */}
        <p className="text-center text-xs text-slate-400 dark:text-slate-500 mt-5">
          Protected by WebGuard · Passive OWASP Security Scanner
        </p>
      </div>
    </div>
  );
}
