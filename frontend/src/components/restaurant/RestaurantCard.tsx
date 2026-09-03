import React from 'react';
import { Link } from 'react-router-dom';
import { Restaurant } from '../../types/restaurant';
import { Star, MapPin, Bookmark } from 'lucide-react';
import { useFavorites } from '../../hooks/useFavorites';
import { useAuth } from '../../hooks/useAuth';

interface RestaurantCardProps {
  restaurant: Restaurant;
}

export const RestaurantCard: React.FC<RestaurantCardProps> = ({ restaurant }) => {
  const { isFavorited, toggleFavorite } = useFavorites();
  const { user } = useAuth();
  const favorited = isFavorited(restaurant.id, undefined);

  const handleFavorite = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!user) {
      alert('Please log in or register to save favorite restaurants!');
      return;
    }
    await toggleFavorite(restaurant.id, undefined);
  };

  return (
    <div className="card-brutal-interactive p-5 flex flex-col justify-between h-full bg-white relative">
      <div>
        {/* Top bar */}
        <div className="flex items-start justify-between gap-3 mb-2">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-black px-2 py-0.5 bg-electric-yellow border border-black">
                {restaurant.price_band}
              </span>
              <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                {restaurant.locality}
              </span>
            </div>
            <h3 className="font-extrabold text-2xl leading-tight font-heading text-ink">
              <Link to={`/restaurants/${restaurant.slug}`} className="hover:text-coral-500 transition-colors">
                {restaurant.name}
              </Link>
            </h3>
          </div>
          <button
            type="button"
            onClick={handleFavorite}
            className={`p-2 border-2 border-black transition-all ${
              favorited
                ? 'bg-coral-500 text-white shadow-brutal-sm'
                : 'bg-white hover:bg-cream-100 text-gray-700'
            }`}
            title={favorited ? 'Remove from favorites' : 'Save to favorites'}
          >
            <Bookmark className={`w-4 h-4 ${favorited ? 'fill-current' : ''}`} />
          </button>
        </div>

        {/* Rating and Reviews */}
        <div className="flex items-center gap-2 mb-3">
          <div className="inline-flex items-center gap-1 px-2 py-0.5 bg-fresh-green text-black border border-black font-black text-xs">
            <Star className="w-3.5 h-3.5 fill-black stroke-black" />
            <span>{restaurant.rating.toFixed(1)}</span>
          </div>
          <span className="text-xs font-bold text-gray-500">
            ({restaurant.review_count} demo reviews)
          </span>
        </div>

        {/* Description */}
        <p className="text-xs text-gray-600 line-clamp-2 mb-4 leading-relaxed">
          {restaurant.description}
        </p>

        {/* Cuisines */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {restaurant.cuisines.map((c) => (
            <span
              key={c}
              className="text-[11px] font-bold px-2 py-0.5 bg-cream-100 border border-black text-gray-800"
            >
              {c}
            </span>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="pt-3 border-t-2 border-black flex items-center justify-between">
        <span className="text-xs font-bold text-gray-500 flex items-center gap-1">
          <MapPin className="w-3.5 h-3.5" />
          {restaurant.locality}
        </span>
        <Link
          to={`/restaurants/${restaurant.slug}`}
          className="btn-brutal text-xs py-1.5 px-3"
        >
          View Menu ({restaurant.menu_items_count ?? 'Explore'})
        </Link>
      </div>
    </div>
  );
};
