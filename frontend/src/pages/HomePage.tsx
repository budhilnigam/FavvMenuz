import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from '../components/search/SearchBar';
import { SuggestionChips } from '../components/search/SuggestionChips';
import { MenuItemCard } from '../components/menu/MenuItemCard';
import { RestaurantCard } from '../components/restaurant/RestaurantCard';
import { searchApi } from '../api/search';
import { restaurantsApi } from '../api/restaurants';
import { SearchSuggestion } from '../types/search';
import { MenuItem, Restaurant } from '../types/restaurant';
import { Sparkles, ShieldAlert, ArrowRight } from 'lucide-react';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [featuredItems, setFeaturedItems] = useState<MenuItem[]>([]);
  const [featuredRestaurants, setFeaturedRestaurants] = useState<Restaurant[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadHomeData() {
      try {
        const [suggData, menuData, restData] = await Promise.all([
          searchApi.getSuggestions(),
          restaurantsApi.listMenuItems({ page: 1 }),
          restaurantsApi.list({ page: 1 }),
        ]);
        setSuggestions(suggData);
        setFeaturedItems(menuData.results.slice(0, 6));
        setFeaturedRestaurants(restData.results.slice(0, 4));
      } catch (err) {
        console.warn('Failed to load initial home data:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadHomeData();
  }, []);

  const handleSearchSubmit = (query: string) => {
    navigate(`/search?query=${encodeURIComponent(query)}`);
  };

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="pt-10 sm:pt-16 pb-8 border-b-3 border-black bg-cream-50 relative overflow-hidden">
        {/* Subtle decorative grid/stripes */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            {/* Tagline Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-electric-yellow border-2 border-black font-black text-xs uppercase tracking-widest shadow-brutal-sm">
              <Sparkles className="w-3.5 h-3.5" />
              AI & Deterministic Food Discovery
            </div>

            {/* Main Title */}
            <h1 className="font-extrabold text-4xl sm:text-6xl md:text-7xl leading-none text-ink tracking-tight font-heading">
              DISCOVER EXACTLY WHAT <br />
              <span className="bg-coral-500 text-white px-3 inline-block transform -rotate-1 border-3 border-black shadow-brutal">
                YOU CRAVE
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-base sm:text-xl font-medium text-gray-700 max-w-2xl mx-auto">
              Natural language queries turned into transparent database searches. Specify budget, dietary tags, spice level, and localities in synthetic Noida.
            </p>

            {/* Search Box */}
            <div className="pt-2 max-w-3xl mx-auto">
              <SearchBar onSearch={handleSearchSubmit} autoFocus />
              {suggestions.length > 0 && (
                <SuggestionChips suggestions={suggestions} onSelect={handleSearchSubmit} />
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Curated Category Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8 pb-3 border-b-3 border-black">
          <div>
            <span className="text-xs font-black uppercase tracking-wider text-coral-500 block mb-1">
              Curated Collections
            </span>
            <h2 className="text-3xl font-black font-heading">Explore By Mood</h2>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: 'Jain Specials', query: 'Jain friendly food without onion garlic', color: 'bg-purple-200' },
            { label: 'Spicy Under ₹300', query: 'Spicy food under 300 rupees', color: 'bg-red-200' },
            { label: 'South Indian Tiffin', query: 'Dosa idli vada in Sector 62', color: 'bg-yellow-200' },
            { label: 'Woodfired Pizza', query: 'Woodfired Italian Pizza under 500', color: 'bg-orange-200' },
            { label: 'Healthy & Vegan', query: 'Healthy vegan protein salad bowls', color: 'bg-green-200' },
            { label: 'Desserts & Kulfi', query: 'Authentic kulfi and gulab jamun under 150', color: 'bg-pink-200' },
          ].map((cat, i) => (
            <button
              key={i}
              type="button"
              onClick={() => handleSearchSubmit(cat.query)}
              className={`${cat.color} p-4 border-3 border-black shadow-brutal hover:shadow-brutal-sm hover:translate-x-1 hover:translate-y-1 transition-all text-left flex flex-col justify-between h-32 group`}
            >
              <span className="font-mono text-xs font-black text-gray-700">0{i + 1}</span>
              <div className="flex items-center justify-between">
                <span className="font-extrabold text-sm sm:text-base leading-tight font-heading">
                  {cat.label}
                </span>
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Popular Demo Dishes */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8 pb-3 border-b-3 border-black">
          <div>
            <span className="text-xs font-black uppercase tracking-wider text-emerald-600 block mb-1">
              Popular Demo Menu Items
            </span>
            <h2 className="text-3xl font-black font-heading">Top Dishes Near You</h2>
          </div>
          <button
            onClick={() => navigate('/search')}
            className="btn-brutal-white text-xs py-1.5 px-3 hidden sm:flex items-center gap-1"
          >
            <span>Browse All Menu</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div key={n} className="h-64 bg-cream-200 border-3 border-black animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredItems.map((item) => (
              <MenuItemCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </section>

      {/* Featured Restaurants */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-end justify-between mb-8 pb-3 border-b-3 border-black">
          <div>
            <span className="text-xs font-black uppercase tracking-wider text-cobalt-600 block mb-1">
              Top Rated Local Hubs
            </span>
            <h2 className="text-3xl font-black font-heading">Fictional Noida Restaurants</h2>
          </div>
          <button
            onClick={() => navigate('/search')}
            className="btn-brutal-white text-xs py-1.5 px-3 hidden sm:flex items-center gap-1"
          >
            <span>Explore Restaurants</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredRestaurants.map((restaurant) => (
            <RestaurantCard key={restaurant.id} restaurant={restaurant} />
          ))}
        </div>
      </section>

      {/* Synthetic Notice Card */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-electric-yellow border-3 border-black p-6 sm:p-8 shadow-brutal flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <h3 className="font-black text-2xl font-heading flex items-center gap-2">
              <ShieldAlert className="w-6 h-6 stroke-[2.5]" />
              Deterministic, Grounded Discovery
            </h3>
            <p className="text-sm font-semibold text-gray-800 leading-relaxed">
              FavvMenuz converts user prompts into structured SearchPlans, applying strict price bounds, allergen exclusions, and dietary tags inside the database. No hallucinations, no inflated claims.
            </p>
          </div>
          <button
            onClick={() => navigate('/search')}
            className="btn-brutal-coral text-sm py-3 px-6 shrink-0"
          >
            Try Natural Search Now
          </button>
        </div>
      </section>
    </div>
  );
};
