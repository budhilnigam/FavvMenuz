import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LogIn, Loader2, AlertCircle } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const from = (location.state as { from?: { pathname?: string } })?.from?.pathname || '/';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please provide both username and password.');
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      await login({ username, password });
      navigate(from, { replace: true });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Invalid username or password.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-16 px-4">
      <div className="card-brutal p-8 bg-white space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-electric-yellow border-2 border-black flex items-center justify-center font-black mx-auto shadow-brutal-sm">
            <LogIn className="w-6 h-6" />
          </div>
          <h1 className="text-3xl font-black font-heading tracking-tight">LOG IN</h1>
          <p className="text-xs font-bold text-gray-600">
            Sign in to access and manage your saved favorite dishes
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border-2 border-black p-3 text-xs font-bold text-red-900 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-coral-500 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="username">
              Username
            </label>
            <input
              id="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="e.g. foodlover"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="btn-brutal w-full py-3 text-sm flex items-center justify-center gap-2 mt-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Signing in...</span>
              </>
            ) : (
              <span>Sign In to FavvMenuz</span>
            )}
          </button>
        </form>

        <div className="pt-4 border-t-2 border-black text-center text-xs font-bold">
          <p className="text-gray-600">
            Don't have an account yet?{' '}
            <Link to="/register" className="text-ink underline hover:text-coral-500">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
