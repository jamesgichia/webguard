import { useState, useEffect } from 'react';
import {
  Key,
  Plus,
  Trash2,
  Loader2,
  Copy,
  Check,
  AlertTriangle,
  ShieldCheck,
  Eye,
  EyeOff,
} from 'lucide-react';
import { api } from '../services/api';
import type { ApiKey } from '../types';
import { timeAgo } from '../utils/helpers';

export default function ApiKeys() {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newKeyValue, setNewKeyValue] = useState<string | null>(null);
  const [copiedKey, setCopiedKey] = useState(false);
  const [revokingId, setRevokingId] = useState<string | null>(null);
  const [showKeyText, setShowKeyText] = useState(false);

  useEffect(() => {
    fetchKeys();
  }, []);

  const fetchKeys = async () => {
    try {
      const res = await api.get('/keys/');
      setKeys(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const createKey = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName.trim()) return;
    setCreating(true);
    try {
      const res = await api.post('/keys/', { name: newKeyName.trim() });
      setNewKeyValue(res.data.key);
      setNewKeyName('');
      setShowCreateForm(false);
      await fetchKeys();
    } catch (err) {
      console.error('Failed to create key:', err);
    } finally {
      setCreating(false);
    }
  };

  const revokeKey = async (id: string) => {
    setRevokingId(id);
    try {
      await api.delete(`/keys/${id}`);
      setKeys((prev) => prev.filter((k) => k.id !== id));
    } catch (err) {
      console.error('Failed to revoke key:', err);
    } finally {
      setRevokingId(null);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedKey(true);
      setTimeout(() => setCopiedKey(false), 2000);
    } catch {
      /* clipboard not available */
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

  return (
    <>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
            API Keys
          </h2>
          <p className="text-slate-500 dark:text-slate-400 mt-1">
            Manage keys for CLI connected mode.
          </p>
        </div>
        <button
          onClick={() => {
            setShowCreateForm(true);
            setNewKeyValue(null);
          }}
          className="btn-primary flex items-center space-x-2 text-sm w-fit"
        >
          <Plus className="w-4 h-4" />
          <span>New API Key</span>
        </button>
      </div>

      {/* Newly created key — show ONCE */}
      {newKeyValue && (
        <div className="glass-card border border-success/30 bg-success/5 p-5 mb-6">
          <div className="flex items-start space-x-3">
            <ShieldCheck className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-semibold text-success mb-1">
                API Key Created — Copy it now!
              </h4>
              <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
                This key is shown <strong>only once</strong> and cannot be retrieved again.
              </p>
              <div className="flex items-center gap-2">
                <div className="flex-1 flex items-center gap-2 bg-slate-100 dark:bg-sentinel-950 border border-slate-200 dark:border-sentinel-700 rounded-xl px-4 py-2.5 font-mono text-sm text-slate-900 dark:text-slate-100 overflow-hidden">
                  <span className="truncate">
                    {showKeyText ? newKeyValue : '•'.repeat(Math.min(newKeyValue.length, 48))}
                  </span>
                </div>
                <button
                  onClick={() => setShowKeyText(!showKeyText)}
                  className="p-2.5 rounded-xl border border-slate-200 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
                  title={showKeyText ? 'Hide key' : 'Show key'}
                >
                  {showKeyText ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
                <button
                  onClick={() => copyToClipboard(newKeyValue)}
                  className="p-2.5 rounded-xl border border-slate-200 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 text-slate-500 hover:text-cyber-500 dark:hover:text-cyber-400 transition-colors"
                  title="Copy key"
                >
                  {copiedKey ? (
                    <Check className="w-4 h-4 text-success" />
                  ) : (
                    <Copy className="w-4 h-4" />
                  )}
                </button>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-3 font-mono">
                Usage: <span className="text-cyber-400">webguard scan run &lt;url&gt; --api-key {newKeyValue.slice(0, 16)}...</span>
              </p>
            </div>
            <button
              onClick={() => setNewKeyValue(null)}
              className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors text-xs"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      {/* Create form */}
      {showCreateForm && !newKeyValue && (
        <div className="glass-card p-5 mb-6">
          <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">
            Create New API Key
          </h4>
          <form onSubmit={createKey} className="flex gap-3">
            <input
              type="text"
              placeholder="Key name (e.g. CI Pipeline, Dev Machine)"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              maxLength={64}
              className="flex-1 rounded-xl border border-slate-300 dark:border-sentinel-700 bg-white dark:bg-sentinel-850 px-4 py-2.5 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:ring-2 focus:ring-cyber-500/50 focus:border-cyber-500 outline-none transition-all duration-200 text-sm"
              autoFocus
            />
            <button
              type="submit"
              disabled={creating || !newKeyName.trim()}
              className="btn-primary text-sm flex items-center space-x-2 disabled:opacity-50 disabled:hover:scale-100"
            >
              {creating ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <span>Create</span>
              )}
            </button>
            <button
              type="button"
              onClick={() => setShowCreateForm(false)}
              className="px-4 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-sentinel-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-sentinel-800 transition-colors"
            >
              Cancel
            </button>
          </form>
        </div>
      )}

      {/* Keys list */}
      {keys.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <Key className="w-12 h-12 text-slate-400 dark:text-slate-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">
            No API keys yet
          </h3>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            Create a key to use WebGuard in connected mode from your CLI or CI pipeline.
          </p>
        </div>
      ) : (
        <div className="glass-card overflow-hidden">
          {/* Warning banner */}
          <div className="flex items-center space-x-2 px-6 py-3 bg-warning/5 border-b border-warning/20">
            <AlertTriangle className="w-4 h-4 text-warning flex-shrink-0" />
            <p className="text-xs text-warning font-medium">
              Treat API keys like passwords — never commit them to source control.
            </p>
          </div>

          <div className="divide-y divide-slate-200 dark:divide-sentinel-700/30">
            {keys.map((apiKey) => (
              <div
                key={apiKey.id}
                className="flex items-center justify-between px-6 py-4 hover:bg-slate-50/50 dark:hover:bg-sentinel-800/20 transition-colors group"
              >
                <div className="flex items-center space-x-4 min-w-0">
                  <div className="w-9 h-9 rounded-xl bg-violet-500/10 dark:bg-violet-500/15 flex items-center justify-center flex-shrink-0">
                    <Key className="w-4 h-4 text-violet-400" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                      {apiKey.name}
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {apiKey.last_used_at
                        ? `Last used ${timeAgo(apiKey.last_used_at)}`
                        : 'Never used'}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="text-right hidden sm:block">
                    <p className="text-xs text-slate-400 dark:text-slate-500">Created</p>
                    <p className="text-xs text-slate-600 dark:text-slate-400 font-mono">
                      {apiKey.id.slice(0, 8)}…
                    </p>
                  </div>
                  <button
                    onClick={() => revokeKey(apiKey.id)}
                    disabled={revokingId === apiKey.id}
                    className="p-2 rounded-xl text-slate-400 hover:text-danger hover:bg-danger/10 transition-all duration-200 opacity-0 group-hover:opacity-100"
                    title="Revoke key"
                  >
                    {revokingId === apiKey.id ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Trash2 className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
