import React, { useState } from 'react';
import { SearchPlan } from '../../types/search';
import { SlidersHorizontal, RotateCcw, ChevronDown, Check } from 'lucide-react';

interface FilterBarProps {
  plan: SearchPlan | null;
  onFilterChange: (updated: Partial<SearchPlan>) => void;
  onReset: () => void;
}

const LOCALITIES = [
  'Sector 18',
  'Sector 62',
  'Sector 137',
  'Sector 50',
  'Sector 76',
  'Sector 104',
  'Noida Expressway',
  'Greater Noida West',
];

const DIETARY_TAGS = [
  { id: 'vegetarian', label: 'Vegetarian' },
  { id: 'jain_friendly', label: 'Jain-Friendly' },
  { id: 'vegan', label: 'Vegan' },
  { id: 'gluten_free', label: 'Gluten-Free' },
  { id: 'dairy_free', label: 'Dairy-Free' },
];

const SPICE_OPTIONS = [
  { id: 'mild', label: 'Mild' },
  { id: 'medium', label: 'Medium' },
  { id: 'spicy', label: 'Spicy' },
  { id: 'extra_spicy', label: 'Extra Spicy' },
];

export const FilterBar: React.FC<FilterBarProps> = ({
  plan,
  onFilterChange,
  onReset,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const activeDietary = plan?.dietary_tags || [];
  const maxPrice = plan?.max_price ?? null;
  const currentLocality = plan?.locality || '';
  const currentSpice = plan?.spice_level || '';
  const currentSort = plan?.sort_by || 'relevance';

  const toggleDietary = (tag: string) => {
    let next: string[];
    if (activeDietary.includes(tag)) {
      next = activeDietary.filter((t) => t !== tag);
    } else {
      next = [...activeDietary, tag];
    }
    onFilterChange({ dietary_tags: next });
  };

  return (
    <div className="bg-white border-3 border-black p-4 shadow-brutal mb-6">
      {/* Top summary row */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-black text-xs uppercase tracking-wider flex items-center gap-1.5 mr-2">
            <SlidersHorizontal className="w-3.5 h-3.5" />
            Active Constraints:
          </span>

          {/* Budget Chip */}
          {maxPrice !== null && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-yellow-100 border-2 border-black font-bold text-xs">
              Under ₹{maxPrice}
            </span>
          )}

          {/* Locality Chip */}
          {currentLocality && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-100 border-2 border-black font-bold text-xs">
              📍 {currentLocality}
            </span>
          )}

          {/* Dietary Chips */}
          {activeDietary.map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 px-2.5 py-1 bg-green-100 border-2 border-black font-bold text-xs"
            >
              ✓ {tag.replace('_', ' ').toUpperCase()}
            </span>
          ))}

          {/* Spice Chip */}
          {currentSpice && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-coral-50 border-2 border-black font-bold text-xs">
              🌶️ {currentSpice.toUpperCase()}
            </span>
          )}

          {/* Distance */}
          {plan?.max_distance_km && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-purple-100 border-2 border-black font-bold text-xs">
              Within {plan.max_distance_km} km
            </span>
          )}
        </div>

        {/* Expand / Collapse & Reset Actions */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onReset}
            className="text-xs font-bold flex items-center gap-1 text-gray-600 hover:text-black px-2 py-1 hover:underline"
          >
            <RotateCcw className="w-3 h-3" />
            Reset
          </button>
          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="btn-brutal-white text-xs py-1 px-3 flex items-center gap-1"
          >
            <span>{isExpanded ? 'Hide Filters' : 'Refine Filters'}</span>
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
          </button>
        </div>
      </div>

      {/* Expanded Controls Panel */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t-2 border-black grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-bold">
          {/* Locality */}
          <div>
            <label className="block uppercase text-gray-500 mb-1.5">Locality</label>
            <select
              value={currentLocality}
              onChange={(e) => onFilterChange({ locality: e.target.value || null })}
              className="w-full bg-cream-50 border-2 border-black p-2 font-bold focus:bg-white"
            >
              <option value="">All Noida</option>
              {LOCALITIES.map((loc) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
          </div>

          {/* Max Budget */}
          <div>
            <label className="block uppercase text-gray-500 mb-1.5">Max Budget (₹)</label>
            <div className="flex items-center gap-1.5">
              {[200, 350, 500, 700].map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => onFilterChange({ max_price: maxPrice === p ? null : p })}
                  className={`flex-1 py-1.5 border-2 border-black text-center ${
                    maxPrice === p ? 'bg-electric-yellow font-black shadow-brutal-sm' : 'bg-white hover:bg-cream-100'
                  }`}
                >
                  ₹{p}
                </button>
              ))}
            </div>
          </div>

          {/* Spice Level */}
          <div>
            <label className="block uppercase text-gray-500 mb-1.5">Spice Level</label>
            <select
              value={currentSpice}
              onChange={(e) => onFilterChange({ spice_level: e.target.value || null })}
              className="w-full bg-cream-50 border-2 border-black p-2 font-bold focus:bg-white"
            >
              <option value="">Any Spice Level</option>
              {SPICE_OPTIONS.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="block uppercase text-gray-500 mb-1.5">Sort Order</label>
            <select
              value={currentSort}
              onChange={(e) => onFilterChange({ sort_by: e.target.value })}
              className="w-full bg-cream-50 border-2 border-black p-2 font-bold focus:bg-white"
            >
              <option value="relevance">Highest Relevance</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating_desc">Highest Demo Rating</option>
              <option value="distance_asc">Nearest Distance</option>
            </select>
          </div>

          {/* Dietary Checkboxes */}
          <div className="md:col-span-4 mt-2 pt-2 border-t border-dashed border-gray-300">
            <span className="block uppercase text-gray-500 mb-2">Dietary Requirements (Strict)</span>
            <div className="flex flex-wrap gap-2">
              {DIETARY_TAGS.map((tag) => {
                const checked = activeDietary.includes(tag.id);
                return (
                  <button
                    key={tag.id}
                    type="button"
                    onClick={() => toggleDietary(tag.id)}
                    className={`inline-flex items-center gap-1 px-3 py-1.5 border-2 border-black ${
                      checked
                        ? 'bg-fresh-green text-black font-black shadow-brutal-sm'
                        : 'bg-white hover:bg-cream-200'
                    }`}
                  >
                    {checked && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                    <span>{tag.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
