import { useState, useCallback } from 'react';
import { SearchResponse, SearchResultItem, SearchPlan } from '../types/search';
import { searchApi, SearchPayload } from '../api/search';

export function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [baseResults, setBaseResults] = useState<SearchResultItem[]>([]);
  const [searchPlan, setSearchPlan] = useState<SearchPlan | null>(null);
  const [searchMode, setSearchMode] = useState<'ai' | 'fallback'>('fallback');
  const [totalResults, setTotalResults] = useState(0);
  const [emptySuggestion, setEmptySuggestion] = useState<string | null>(null);
  const [aiMessage, setAiMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const applyLocalFilters = useCallback((baseResults: SearchResultItem[], plan: SearchPlan): SearchResultItem[] => {
    const filtered = baseResults.filter(({ item, restaurant, distance_km }) => {
      if (plan.max_price !== null && item.price_paise / 100 > plan.max_price) return false;
      if (plan.min_price !== null && item.price_paise / 100 < plan.min_price) return false;
      if (plan.locality && restaurant.locality.toLowerCase() !== plan.locality.toLowerCase()) return false;
      if (plan.spice_level && item.spice_level !== plan.spice_level) return false;
      if (plan.max_distance_km !== null && (distance_km === null || distance_km > plan.max_distance_km)) return false;
      if (!plan.dietary_tags.every((tag) => item.dietary_tags.includes(tag))) return false;
      return true;
    });

    if (plan.sort_by === 'price_asc') filtered.sort((a, b) => a.item.price_paise - b.item.price_paise);
    else if (plan.sort_by === 'price_desc') filtered.sort((a, b) => b.item.price_paise - a.item.price_paise);
    else if (plan.sort_by === 'rating_desc') filtered.sort((a, b) => b.restaurant.rating - a.restaurant.rating);
    else if (plan.sort_by === 'distance_asc') filtered.sort((a, b) => (a.distance_km ?? 999) - (b.distance_km ?? 999));
    else filtered.sort((a, b) => b.relevance_score - a.relevance_score);
    return filtered;
  }, []);

  const execute = useCallback(async (payload: SearchPayload) => {
    setIsLoading(true);
    setError(null);
    try {
      const response: SearchResponse = await searchApi.executeSearch(payload);
      setBaseResults(response.results);
      setResults(response.results);
      setSearchPlan(response.search_plan);
      setSearchMode(response.search_mode);
      setTotalResults(response.total_results);
      setEmptySuggestion(response.empty_suggestion);
      setAiMessage(response.ai_message || null);
      if (payload.query !== undefined) {
        setQuery(payload.query);
      }
      return response;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Search failed. Please try again.';
      setError(msg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const refine = useCallback((updated: Partial<SearchPlan>) => {
    if (!searchPlan) return;
    const nextPlan = { ...searchPlan, ...updated };
    const nextResults = applyLocalFilters(baseResults, nextPlan);
    setSearchPlan(nextPlan);
    setResults(nextResults);
    setTotalResults(nextResults.length);
    setEmptySuggestion(nextResults.length ? null : 'Try broadening one of the active filters.');
  }, [applyLocalFilters, baseResults, searchPlan]);

  return {
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
  };
}
