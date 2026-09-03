import React from 'react';
import { Link } from 'react-router-dom';
import { MenuItem } from '../../types/restaurant';
import { formatCurrencyFromPaise, getSpiceBadgeDetails, getDietaryTagStyle } from '../../utils/format';
import { Bookmark, Sparkles, MapPin } from 'lucide-react';
import { useFavorites } from '../../hooks/useFavorites';
import { useAuth } from '../../hooks/useAuth';

interface MenuItemCardProps {
  item: MenuItem;
  matchReasons?: string[];
  distanceKm?: number | null;
}

export const MenuItemCard: React.FC<MenuItemCardProps> = ({
  item,
  matchReasons = [],
  distanceKm,
}) => {
  const { isFavorited, toggleFavorite } = useFavorites();
  const { user } = useAuth();
  const favorited = isFavorited(undefined, item.id);

  const handleFavorite = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!user) {
      alert('Please log in or register to save favorite dishes!');
      return;
    }
    await toggleFavorite(undefined, item.id);
  };

  const spice = getSpiceBadgeDetails(item.spice_level);

  return (
    <div className="card-brutal-interactive p-5 flex flex-col justify-between h-full bg-white relative">
      {/* Top Header */}
      <div>
        <div className="flex items-start justify-between gap-3 mb-2">
          <div>
            <span className="text-[11px] font-black uppercase tracking-wider px-2 py-0.5 bg-cream-200 border border-black inline-block mb-1">
              {item.category}
            </span>
            <h3 className="font-extrabold text-xl leading-tight font-heading text-ink">
              {item.name}
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

        {/* Restaurant link & Locality */}
        <div className="flex items-center gap-2 text-xs font-bold text-gray-700 mb-3">
          <Link
            to={`/restaurants/${item.restaurant_slug || ''}`}
            className="text-ink hover:underline font-extrabold hover:text-coral-500"
          >
            {item.restaurant_name}
          </Link>
          <span>•</span>
          <span className="flex items-center gap-0.5">
            <MapPin className="w-3.5 h-3.5 text-gray-500" />
            {item.restaurant_locality}
            {distanceKm !== null && distanceKm !== undefined && (
              <span className="ml-1 text-gray-500">({distanceKm.toFixed(1)} km)</span>
            )}
          </span>
        </div>

        {/* Description */}
        <p className="text-xs text-gray-600 line-clamp-2 mb-4 leading-relaxed">
          {item.description}
        </p>

        {/* Ingredients */}
        {item.ingredients && item.ingredients.length > 0 && (
          <div className="mb-4">
            <span className="text-[10px] font-black uppercase tracking-wider text-gray-400 block mb-1">
              Ingredients:
            </span>
            <p className="text-xs font-semibold text-gray-800 line-clamp-1">
              {item.ingredients.join(', ')}
            </p>
          </div>
        )}

        {/* Dietary & Spice Tags */}
        <div className="flex flex-wrap items-center gap-1.5 mb-4">
          {item.dietary_tags.map((tag) => {
            const style = getDietaryTagStyle(tag);
            return (
              <span
                key={tag}
                className={`text-[11px] font-black uppercase px-2 py-0.5 border border-black ${style.bgClass} ${style.textClass}`}
              >
                {style.label}
              </span>
            );
          })}
          <span className={`text-[11px] font-bold px-2 py-0.5 border ${spice.colorClass}`}>
            🌶️ {spice.label}
          </span>
        </div>

        {/* Match Explanations (Grounded in query) */}
        {matchReasons.length > 0 && (
          <div className="bg-yellow-50/80 border-2 border-dashed border-black/50 p-2.5 mb-4 space-y-1">
            <span className="text-[10px] font-black uppercase tracking-wider text-black flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-500" />
              Why this matches:
            </span>
            {matchReasons.map((reason, i) => (
              <p key={i} className="text-xs font-bold text-gray-800 flex items-center gap-1">
                <span className="text-coral-500 font-black">•</span> {reason}
              </p>
            ))}
          </div>
        )}
      </div>

      {/* Footer: Price & Details Link */}
      <div className="pt-3 border-t-2 border-black flex items-center justify-between">
        <div className="font-heading font-black text-2xl text-ink">
          {formatCurrencyFromPaise(item.price_paise)}
        </div>
        <Link
          to={`/restaurants/${item.restaurant_slug || ''}`}
          className="btn-brutal text-xs py-1.5 px-3"
        >
          View Restaurant
        </Link>
      </div>
    </div>
  );
};
