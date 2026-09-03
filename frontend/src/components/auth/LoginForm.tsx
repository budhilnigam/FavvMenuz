import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Loader2, AlertCircle } from 'lucide-react';

interface LoginFormProps {
  onSuccess?: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess }) => {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please provide username and password.');
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      await login({ username, password });
      onSuccess?.();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Invalid credentials.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border-2 border-black p-3 text-xs font-bold text-red-900 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-coral-500 shrink-0" />
          <span>{error}</span>
        </div>
      )}
      <div>
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="auth-username">
          Username
        </label>
        <input
          id="auth-username"
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="auth-password">
          Password
        </label>
        <input
          id="auth-password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="btn-brutal w-full py-2.5 text-sm flex items-center justify-center gap-2"
      >
        {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Sign In'}
      </button>
    </form>
  );
};
