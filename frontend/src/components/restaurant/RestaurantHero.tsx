import React from 'react';
import { Restaurant } from '../../types/restaurant';
import { Star, MapPin, Bookmark, ShieldAlert } from 'lucide-react';

interface RestaurantHeroProps {
  restaurant: Restaurant;
  isFavorited: boolean;
  onToggleFavorite: () => void;
}

export const RestaurantHero: React.FC<RestaurantHeroProps> = ({
  restaurant,
  isFavorited,
  onToggleFavorite,
}) => {
  return (
    <div className="card-brutal p-6 sm:p-10 bg-white space-y-6 relative">
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
        <div className="space-y-3 max-w-3xl">
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

          <h1 className="text-3xl sm:text-5xl font-black font-heading text-ink leading-tight">
            {restaurant.name}
          </h1>

          <p className="text-xs sm:text-sm font-semibold text-gray-600">
            {restaurant.address}
          </p>

          <p className="text-sm font-medium text-gray-700 leading-relaxed">
            {restaurant.description}
          </p>

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
            onClick={onToggleFavorite}
            className={`btn-brutal text-xs flex items-center gap-1.5 py-2 px-4 ${
              isFavorited ? 'bg-coral-500 text-white' : 'bg-electric-yellow'
            }`}
          >
            <Bookmark className={`w-4 h-4 ${isFavorited ? 'fill-current' : ''}`} />
            <span>{isFavorited ? 'Favorited' : 'Bookmark Restaurant'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
