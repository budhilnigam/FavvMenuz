import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Loader2, AlertCircle } from 'lucide-react';
import { validatePassword } from '../../utils/validation';

interface RegisterFormProps {
  onSuccess?: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess }) => {
  const { register } = useAuth();
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
      onSuccess?.();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Registration failed.');
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
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="rf-username">
          Username *
        </label>
        <input
          id="rf-username"
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="rf-email">
          Email (Optional)
        </label>
        <input
          id="rf-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="rf-password">
          Password *
        </label>
        <input
          id="rf-password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <div>
        <label className="block text-xs font-black uppercase tracking-wider mb-1" htmlFor="rf-confirm">
          Confirm Password *
        </label>
        <input
          id="rf-confirm"
          type="password"
          required
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
          className="w-full bg-cream-50 border-2 border-black p-2.5 font-bold text-sm"
        />
      </div>
      <button
        type="submit"
        disabled={isSubmitting}
        className="btn-brutal-coral w-full py-2.5 text-sm flex items-center justify-center gap-2"
      >
        {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Create Account'}
      </button>
    </form>
  );
};
