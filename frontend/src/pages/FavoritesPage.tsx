import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useFavorites } from '../hooks/useFavorites';
import { MenuItemCard } from '../components/menu/MenuItemCard';
import { RestaurantCard } from '../components/restaurant/RestaurantCard';
import { Bookmark, Lock, Trash2, ArrowRight } from 'lucide-react';

export const FavoritesPage: React.FC = () => {
  const { user } = useAuth();
  const { favorites, isLoading, removeFavorite } = useFavorites();

  if (!user) {
    return (
      <div className="max-w-xl mx-auto py-20 px-4 text-center space-y-6">
        <div className="w-16 h-16 bg-cream-200 border-3 border-black flex items-center justify-center mx-auto shadow-brutal">
          <Lock className="w-8 h-8 text-ink" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-black font-heading">
          SIGN IN TO VIEW SAVED ITEMS
        </h1>
        <p className="text-sm font-medium text-gray-700">
          Save restaurants and dishes to your personal account. No public access or cross-user leaks.
        </p>
        <div className="flex justify-center gap-3 pt-2">
          <Link to="/login" className="btn-brutal text-sm py-2 px-6">
            Log In
          </Link>
          <Link to="/register" className="btn-brutal-white text-sm py-2 px-6">
            Create Free Account
          </Link>
        </div>
      </div>
    );
  }

  const savedRestaurants = favorites
    .filter((f) => f.restaurant_details)
    .map((f) => ({ favId: f.id, data: f.restaurant_details! }));

  const savedDishes = favorites
    .filter((f) => f.menu_item_details)
    .map((f) => ({ favId: f.id, data: f.menu_item_details! }));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Header */}
      <div className="border-b-3 border-black pb-4 flex flex-wrap items-end justify-between gap-4">
        <div>
          <span className="text-xs font-black uppercase tracking-wider text-coral-500 block mb-1">
            Personal Saved Collection
          </span>
          <h1 className="text-3xl sm:text-5xl font-black font-heading flex items-center gap-3">
            <Bookmark className="w-8 h-8 fill-coral-500 text-black" />
            YOUR FAVORITES
          </h1>
        </div>
        <span className="font-mono text-xs font-bold px-3 py-1 bg-cream-200 border-2 border-black">
          Logged in as: {user.username}
        </span>
      </div>

      {isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((n) => (
            <div key={n} className="h-64 bg-cream-200 border-3 border-black animate-pulse" />
          ))}
        </div>
      )}

      {!isLoading && favorites.length === 0 && (
        <div className="card-brutal p-12 text-center max-w-xl mx-auto space-y-4">
          <div className="w-16 h-16 bg-cream-100 border-2 border-black flex items-center justify-center mx-auto shadow-brutal-sm">
            <Bookmark className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-2xl font-black font-heading">No Saved Favorites Yet</h3>
          <p className="text-sm font-medium text-gray-600">
            Bookmark dishes and restaurants as you browse to save them here for quick access.
          </p>
          <Link to="/search" className="btn-brutal text-xs py-2 px-4 inline-flex items-center gap-1.5 mt-2">
            <span>Explore Discovery</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      )}

      {/* Saved Dishes Section */}
      {!isLoading && savedDishes.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-black font-heading border-b-2 border-black pb-2">
            Saved Dishes ({savedDishes.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedDishes.map(({ favId, data }) => (
              <div key={favId} className="relative group">
                <MenuItemCard item={data} />
                <button
                  onClick={() => removeFavorite(favId)}
                  className="absolute bottom-4 right-32 text-xs font-bold text-red-600 hover:underline flex items-center gap-1 bg-white px-2 py-1 border border-black"
                  title="Remove from favorites"
                >
                  <Trash2 className="w-3 h-3" />
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Saved Restaurants Section */}
      {!isLoading && savedRestaurants.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-black font-heading border-b-2 border-black pb-2">
            Saved Restaurants ({savedRestaurants.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedRestaurants.map(({ favId, data }) => (
              <div key={favId} className="relative">
                <RestaurantCard restaurant={data} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
