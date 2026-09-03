import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useFavorites } from '../../hooks/useFavorites';
import { Bookmark, Compass, Search, LogOut } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { favorites } = useFavorites();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 bg-white border-b-3 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 bg-electric-yellow border-2 border-black flex items-center justify-center font-black text-xl shadow-[3px_3px_0px_#000] group-hover:rotate-6 transition-transform">
            FM
          </div>
          <span className="font-extrabold text-2xl tracking-tighter text-ink font-heading">
            FAVV<span className="text-coral-500">MENUZ</span>
          </span>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 font-bold text-sm tracking-wide">
          <Link
            to="/"
            className={`flex items-center gap-1.5 px-3 py-1.5 border-2 border-transparent transition-all ${
              isActive('/') ? 'border-black bg-cream-200 shadow-brutal-sm' : 'hover:border-black'
            }`}
          >
            <Compass className="w-4 h-4" />
            Discover
          </Link>
          <Link
            to="/search"
            className={`flex items-center gap-1.5 px-3 py-1.5 border-2 border-transparent transition-all ${
              isActive('/search') ? 'border-black bg-cream-200 shadow-brutal-sm' : 'hover:border-black'
            }`}
          >
            <Search className="w-4 h-4" />
            Search
          </Link>
          <Link
            to="/favorites"
            className={`flex items-center gap-1.5 px-3 py-1.5 border-2 border-transparent transition-all relative ${
              isActive('/favorites') ? 'border-black bg-cream-200 shadow-brutal-sm' : 'hover:border-black'
            }`}
          >
            <Bookmark className="w-4 h-4" />
            Favorites
            {favorites.length > 0 && (
              <span className="ml-1 bg-coral-500 text-white text-xs px-1.5 py-0.2 font-black border border-black rounded-none">
                {favorites.length}
              </span>
            )}
          </Link>
        </nav>

        {/* User / Authentication Actions */}
        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              <span className="hidden sm:inline-block font-bold text-xs uppercase px-2.5 py-1 bg-cream-200 border-2 border-black">
                {user.username}
              </span>
              <button
                onClick={handleLogout}
                className="btn-brutal-white text-xs flex items-center gap-1 py-1.5"
                title="Log out"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login" className="btn-brutal-white text-xs py-1.5 px-3">
                Login
              </Link>
              <Link to="/register" className="btn-brutal text-xs py-1.5 px-3">
                Join Free
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
