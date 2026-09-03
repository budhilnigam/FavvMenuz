import React from 'react';
import { Link } from 'react-router-dom';
import { Home, Compass } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="max-w-xl mx-auto py-24 px-4 text-center space-y-6">
      <div className="inline-block bg-electric-yellow border-3 border-black p-4 font-black font-heading text-6xl shadow-brutal transform -rotate-3">
        404
      </div>
      <h1 className="text-4xl font-black font-heading">PAGE NOT FOUND</h1>
      <p className="text-base font-semibold text-gray-700">
        The dish or restaurant page you're searching for wandered off the menu.
      </p>
      <div className="flex justify-center gap-4 pt-4">
        <Link to="/" className="btn-brutal text-sm py-2 px-5 flex items-center gap-1.5">
          <Home className="w-4 h-4" />
          Go Home
        </Link>
        <Link to="/search" className="btn-brutal-white text-sm py-2 px-5 flex items-center gap-1.5">
          <Compass className="w-4 h-4" />
          Discovery Search
        </Link>
      </div>
    </div>
  );
};
