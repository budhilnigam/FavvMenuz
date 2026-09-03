import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { restaurantsApi } from '../api/restaurants';
import { Restaurant, MenuItem } from '../types/restaurant';
import { MenuItemCard } from '../components/menu/MenuItemCard';
import { Star, MapPin, Bookmark, ArrowLeft, Loader2, ShieldAlert } from 'lucide-react';
import { useFavorites } from '../../src/hooks/useFavorites';
import { useAuth } from '../../src/hooks/useAuth';

export const RestaurantPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const { isFavorited, toggleFavorite } = useFavorites();
  const { user } = useAuth();
  const favorited = restaurant ? isFavorited(restaurant.id, undefined) : false;

  useEffect(() => {
    if (!slug) return;
    setIsLoading(true);
    restaurantsApi
      .getDetail(slug)
      .then((data) => {
        setRestaurant(data);
        setError(null);
      })
      .catch((err) => {
        setError(err.message || 'Restaurant not found');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [slug]);

  if (isLoading) {
    return (
      <div className="min-h-[50vh] flex items-center justify-center">
        <div className="flex items-center gap-3 font-bold text-lg font-heading">
          <Loader2 className="w-6 h-6 animate-spin text-coral-500" />
          <span>Loading restaurant menu...</span>
        </div>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      <div className="max-w-xl mx-auto py-16 px-4 text-center space-y-4">
        <h2 className="text-3xl font-black font-heading">Restaurant Not Found</h2>
        <p className="text-gray-600 font-medium">{error || 'The requested listing could not be found.'}</p>
        <Link to="/search" className="btn-brutal text-sm inline-block">
          Back to Discovery
        </Link>
      </div>
    );
  }

  const menuItems: MenuItem[] = restaurant.menu_items || [];
  const categories = ['All', ...Array.from(new Set(menuItems.map((item) => item.category)))];

  const filteredItems =
    selectedCategory === 'All'
      ? menuItems
      : menuItems.filter((item) => item.category === selectedCategory);

  const handleFavoriteRestaurant = async () => {
    if (!user) {
      alert('Please log in or register to favorite this restaurant.');
      return;
    }
    await toggleFavorite(restaurant.id, undefined);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Back Link */}
      <Link
        to="/search"
        className="inline-flex items-center gap-1.5 text-xs font-black uppercase tracking-wider text-gray-700 hover:text-black hover:underline"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Discovery
      </Link>

      {/* Restaurant Hero Banner */}
      <div className="card-brutal p-6 sm:p-10 bg-white space-y-6 relative">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            {/* Badges */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-black px-2.5 py-0.5 bg-electric-yellow border-2 border-black">
                {restaurant.price_band}
              </span>
              <span className="text-xs font-black px-2.5 py-0.5 bg-cream-200 border-2 border-black flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5" />
                {restaurant.locality}
              </span>
              <span className="text-xs font-black px-2.5 py-0.5 bg-amber-100 border-2 border-black flex items-center gap-1">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-700" />
                Simulated Demo Listing
              </span>
            </div>

            {/* Restaurant Name */}
            <h1 className="text-3xl sm:text-5xl font-black font-heading text-ink leading-tight">
              {restaurant.name}
            </h1>

            {/* Address */}
            <p className="text-xs sm:text-sm font-semibold text-gray-600">
              {restaurant.address}
            </p>

            {/* Description */}
            <p className="text-sm font-medium text-gray-700 leading-relaxed">
              {restaurant.description}
            </p>

            {/* Cuisines */}
            <div className="flex flex-wrap gap-2 pt-1">
              {restaurant.cuisines.map((c) => (
                <span
                  key={c}
                  className="text-xs font-black px-2 py-0.5 bg-gray-100 border border-black"
                >
                  {c}
                </span>
              ))}
            </div>
          </div>

          {/* Action & Rating Card */}
          <div className="flex md:flex-col items-center md:items-end justify-between gap-4 shrink-0">
            <div className="text-right">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-fresh-green border-2 border-black font-black text-sm shadow-brutal-sm">
                <Star className="w-4 h-4 fill-black stroke-black" />
                <span>{restaurant.rating.toFixed(1)} ★</span>
              </div>
              <span className="block text-xs font-bold text-gray-500 mt-1">
                {restaurant.review_count} synthetic reviews
              </span>
            </div>

            <button
              onClick={handleFavoriteRestaurant}
              className={`btn-brutal text-xs flex items-center gap-1.5 py-2 px-4 ${
                favorited ? 'bg-coral-500 text-white' : 'bg-electric-yellow'
              }`}
            >
              <Bookmark className={`w-4 h-4 ${favorited ? 'fill-current' : ''}`} />
              <span>{favorited ? 'Favorited' : 'Bookmark Restaurant'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Menu Categories Tabs */}
      <div className="space-y-4">
        <div className="flex items-center justify-between pb-2 border-b-3 border-black">
          <h2 className="text-2xl sm:text-3xl font-black font-heading">
            Full Restaurant Menu ({menuItems.length} Dishes)
          </h2>
        </div>

        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setSelectedCategory(cat)}
              className={`px-3.5 py-1.5 border-2 border-black font-extrabold text-xs tracking-wide transition-all ${
                selectedCategory === cat
                  ? 'bg-electric-yellow shadow-brutal-sm -translate-y-0.5'
                  : 'bg-white hover:bg-cream-100'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Menu Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredItems.map((item) => (
          <MenuItemCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
};
