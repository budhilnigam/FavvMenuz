import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { UserPlus, Loader2, AlertCircle } from 'lucide-react';
import { validatePassword } from '../utils/validation';

export const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password || !passwordConfirm) {
      setError('Please complete all required fields.');
      return;
    }
    const pwdCheck = validatePassword(password);
    if (!pwdCheck.isValid) {
      setError(pwdCheck.error || 'Password does not meet requirements.');
      return;
    }
    if (password !== passwordConfirm) {
      setError('Passwords do not match.');
      return;
    }

    setError(null);
    setIsSubmitting(true);
    try {
      await register({
        username,
        email,
        password,
        password_confirm: passwordConfirm,
      });
      navigate('/', { replace: true });
    } catch (err: unknown) {
      const data = (err as { data?: Record<string, unknown> })?.data;
      if (typeof data === 'object' && data !== null) {
        const firstKey = Object.keys(data)[0];
        const val = Array.isArray(data[firstKey]) ? data[firstKey][0] : data[firstKey];
        setError(`${firstKey}: ${String(val)}`);
      } else {
        setError(err instanceof Error ? err.message : 'Registration failed.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-16 px-4">
      <div className="card-brutal p-8 bg-white space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-coral-500 text-white border-2 border-black flex items-center justify-center font-black mx-auto shadow-brutal-sm">
            <UserPlus className="w-6 h-6" />
          </div>
          <h1 className="text-3xl font-black font-heading tracking-tight">JOIN FAVVMENUZ</h1>
          <p className="text-xs font-bold text-gray-600">
            Create your account to save favorites and bookmark discovery plans
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
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="reg-username">
              Username *
            </label>
            <input
              id="reg-username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="e.g. foodexplorer"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="reg-email">
              Email (Optional)
            </label>
            <input
              id="reg-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="explorer@example.com"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="reg-password">
              Password (Min 8 Characters) *
            </label>
            <input
              id="reg-password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="••••••••"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider mb-1.5" htmlFor="reg-confirm">
              Confirm Password *
            </label>
            <input
              id="reg-confirm"
              type="password"
              required
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
              className="w-full bg-cream-50 border-2 border-black p-3 font-bold text-sm focus:bg-white"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="btn-brutal-coral w-full py-3 text-sm flex items-center justify-center gap-2 mt-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Creating Account...</span>
              </>
            ) : (
              <span>Create Account</span>
            )}
          </button>
        </form>

        <div className="pt-4 border-t-2 border-black text-center text-xs font-bold">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-ink underline hover:text-coral-500">
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
