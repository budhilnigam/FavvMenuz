import React, { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useSearch } from '../hooks/useSearch';
import { SearchBar } from '../components/search/SearchBar';
import { SuggestionChips } from '../components/search/SuggestionChips';
import { FilterBar } from '../components/search/FilterBar';
import { ModeBadge } from '../components/search/ModeBadge';
import { MenuItemCard } from '../components/menu/MenuItemCard';
import { searchApi } from '../api/search';
import { SearchSuggestion, SearchPlan } from '../types/search';
import { Utensils, AlertTriangle, RefreshCw, SearchX, Sparkles } from 'lucide-react';

export const SearchPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialQuery = searchParams.get('query') || '';
  const initialLocality = searchParams.get('locality') || null;
  const initialDietary = searchParams.get('dietary') ? [searchParams.get('dietary')!] : [];

  const {
    query,
    setQuery,
    results,
    searchPlan,
    searchMode,
    totalResults,
    emptySuggestion,
    aiMessage,
    isLoading,
    error,
    execute,
    refine,
  } = useSearch();

  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);

  // Load suggestions
  useEffect(() => {
    searchApi.getSuggestions().then(setSuggestions).catch(console.warn);
  }, []);

  const triggerSearch = useCallback((newQuery: string, overrides: Partial<SearchPlan> = {}) => {
    setQuery(newQuery);
    setSearchParams({ query: newQuery });
    execute({
      query: newQuery,
      locality: overrides.locality !== undefined ? overrides.locality : searchPlan?.locality,
      dietary_tags: overrides.dietary_tags !== undefined ? overrides.dietary_tags : searchPlan?.dietary_tags,
      max_price: overrides.max_price !== undefined ? overrides.max_price : searchPlan?.max_price,
      spice_level: overrides.spice_level !== undefined ? overrides.spice_level : searchPlan?.spice_level,
      max_distance_km: overrides.max_distance_km !== undefined ? overrides.max_distance_km : searchPlan?.max_distance_km,
      sort_by: overrides.sort_by || searchPlan?.sort_by || 'relevance',
    });
  }, [execute, searchPlan, setSearchParams, setQuery]);

  // Run initial search from URL params
  useEffect(() => {
    if (initialQuery || initialLocality || initialDietary.length > 0) {
      execute({
        query: initialQuery,
        locality: initialLocality,
        dietary_tags: initialDietary,
      });
    } else {
      // Default initial query for discovery
      execute({ query: 'Spicy vegetarian dishes under 350' });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleFilterUpdate = (updated: Partial<SearchPlan>) => {
    refine(updated);
  };

  const handleResetFilters = () => {
    refine({
      locality: null,
      dietary_tags: [],
      max_price: null,
      min_price: null,
      spice_level: null,
      max_distance_km: null,
      sort_by: 'relevance',
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Search Header */}
      <div className="space-y-4">
        <h1 className="text-3xl sm:text-5xl font-black font-heading tracking-tight">
          DISCOVER & FILTER
        </h1>
        <SearchBar
          initialQuery={query || initialQuery}
          onSearch={(q) => triggerSearch(q)}
          isLoading={isLoading}
        />
        {suggestions.length > 0 && (
          <SuggestionChips suggestions={suggestions} onSelect={(q) => triggerSearch(q)} />
        )}
      </div>

      {/* Filter and Mode Bar */}
      <FilterBar
        plan={searchPlan}
        onFilterChange={handleFilterUpdate}
        onReset={handleResetFilters}
      />

      {/* Results Header: Count & Mode Badge */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-2 border-b-2 border-black">
        <div className="flex items-center gap-3">
          <h2 className="text-xl sm:text-2xl font-black font-heading flex items-center gap-2">
            <Utensils className="w-5 h-5" />
            <span>{isLoading ? 'Searching...' : `${totalResults} Dishes Found`}</span>
          </h2>
          {query && (
            <span className="text-xs font-bold text-gray-500 hidden sm:inline">
              for "{query}"
            </span>
          )}
        </div>

        {/* AI vs Fallback Mode Badge */}
        <ModeBadge mode={searchMode} />
      </div>

      {aiMessage && (
        <div className="bg-electric-yellow border-2 border-black px-4 py-3 text-sm font-bold shadow-brutal-sm">
          {aiMessage}
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-3 border-black p-6 shadow-brutal flex items-start gap-4">
          <AlertTriangle className="w-6 h-6 text-coral-500 shrink-0 mt-0.5" />
          <div className="space-y-2">
            <h3 className="font-black text-lg font-heading text-red-900">Search Encountered an Issue</h3>
            <p className="text-sm font-semibold text-red-800">{error}</p>
            <button
              onClick={() => triggerSearch(query)}
              className="btn-brutal-white text-xs py-1.5 px-3 flex items-center gap-1.5 mt-2"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Retry Search
            </button>
          </div>
        </div>
      )}

      {/* Loading Skeletons */}
      {isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((n) => (
            <div key={n} className="h-72 bg-cream-200 border-3 border-black animate-pulse" />
          ))}
        </div>
      )}

      {/* Results Grid */}
      {!isLoading && !error && results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map(({ item, match_reasons, distance_km }) => (
            <MenuItemCard
              key={item.id}
              item={item}
              matchReasons={match_reasons}
              distanceKm={distance_km}
            />
          ))}
        </div>
      )}

      {/* Empty Results State with Grounded Suggestions */}
      {!isLoading && !error && results.length === 0 && (
        <div className="card-brutal p-8 sm:p-12 text-center max-w-2xl mx-auto space-y-4 bg-white">
          <div className="w-16 h-16 bg-cream-200 border-2 border-black flex items-center justify-center mx-auto shadow-brutal-sm">
            <SearchX className="w-8 h-8 text-ink" />
          </div>
          <h3 className="text-2xl font-black font-heading">No Matches Found</h3>
          <p className="text-sm font-medium text-gray-700">
            We couldn't find any dishes strictly satisfying all active constraints. Hard constraints are never relaxed silently.
          </p>

          {emptySuggestion && (
            <div className="bg-electric-yellow/20 border-2 border-black p-4 text-xs font-bold text-ink space-y-1">
              <span className="font-black flex items-center justify-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                Suggestion to broaden results:
              </span>
              <p>{emptySuggestion}</p>
            </div>
          )}

          <div className="pt-4 flex flex-wrap justify-center gap-3">
            <button
              onClick={handleResetFilters}
              className="btn-brutal text-xs py-2 px-4"
            >
              Clear Specific Filters
            </button>
            <button
              onClick={() => triggerSearch('Vegetarian dishes under 400')}
              className="btn-brutal-white text-xs py-2 px-4"
            >
              Try Popular Default
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
