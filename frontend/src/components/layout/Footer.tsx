import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, ShieldCheck, Terminal } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t-3 border-black mt-20 pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Col 1: Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-electric-yellow border-2 border-black flex items-center justify-center font-black text-sm shadow-[2px_2px_0px_#000]">
                FM
              </div>
              <span className="font-extrabold text-xl tracking-tight font-heading">
                FAVV<span className="text-coral-500">MENUZ</span>
              </span>
            </div>
            <p className="text-sm font-medium text-gray-700 leading-relaxed">
              An intelligent, transparent natural-language food discovery engine. Find exactly what you crave by budget, cuisine, dietary tags, and locality.
            </p>
          </div>

          {/* Col 2: Localities */}
          <div>
            <h4 className="font-black text-xs uppercase tracking-wider mb-4 border-b-2 border-black pb-1 inline-block">
              Noida Localities
            </h4>
            <ul className="space-y-2 text-sm font-semibold">
              <li><Link to="/search?locality=Sector 18" className="hover:underline">Sector 18 (Hub)</Link></li>
              <li><Link to="/search?locality=Sector 62" className="hover:underline">Sector 62 (Corporate)</Link></li>
              <li><Link to="/search?locality=Sector 137" className="hover:underline">Sector 137 (Expressway)</Link></li>
              <li><Link to="/search?locality=Sector 104" className="hover:underline">Sector 104 (Boulevard)</Link></li>
              <li><Link to="/search?locality=Greater Noida West" className="hover:underline">Greater Noida West</Link></li>
            </ul>
          </div>

          {/* Col 3: Cuisines & Diets */}
          <div>
            <h4 className="font-black text-xs uppercase tracking-wider mb-4 border-b-2 border-black pb-1 inline-block">
              Dietary & Categories
            </h4>
            <ul className="space-y-2 text-sm font-semibold">
              <li><Link to="/search?dietary=vegetarian" className="hover:underline">Vegetarian Specials</Link></li>
              <li><Link to="/search?dietary=jain_friendly" className="hover:underline">Strict Jain-Friendly</Link></li>
              <li><Link to="/search?dietary=vegan" className="hover:underline">100% Plant-Based Vegan</Link></li>
              <li><Link to="/search?dietary=gluten_free" className="hover:underline">Gluten-Free Options</Link></li>
              <li><Link to="/search?query=dosa under 200" className="hover:underline">South Indian Tiffin</Link></li>
            </ul>
          </div>

          {/* Col 4: Architecture & Demo Policy */}
          <div className="bg-cream-100 p-4 border-2 border-black shadow-brutal-sm">
            <h4 className="font-black text-xs uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              Demo Data Policy
            </h4>
            <p className="text-xs text-gray-700 leading-normal mb-3">
              All 50 restaurants, 600+ dishes, prices and coordinates are entirely synthetic simulations. No live payments or actual delivery.
            </p>
            <div className="text-[11px] font-mono text-gray-600 flex items-center gap-1">
              <Terminal className="w-3.5 h-3.5" />
              Django ORM + Caddy + Redis
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t-2 border-black pt-6 flex flex-col sm:flex-row items-center justify-between text-xs font-bold gap-4">
          <p>© {new Date().getFullYear()} FavvMenuz. Built with Django, React, Tailwind & Vite.</p>
          <div className="flex items-center gap-4">
            <a href="/admin/" className="hover:underline text-gray-700">Admin Portal</a>
            <span>•</span>
            <span className="flex items-center gap-1">
              Made with <Heart className="w-3.5 h-3.5 text-coral-500 fill-coral-500" /> for discovery
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
