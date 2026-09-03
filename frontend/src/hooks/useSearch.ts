import { useState, useCallback } from 'react';
import { SearchResponse, SearchResultItem, SearchPlan } from '../types/search';
import { searchApi, SearchPayload } from '../api/search';

export function useSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [searchPlan, setSearchPlan] = useState<SearchPlan | null>(null);
  const [searchMode, setSearchMode] = useState<'ai' | 'fallback'>('fallback');
  const [totalResults, setTotalResults] = useState(0);
  const [emptySuggestion, setEmptySuggestion] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (payload: SearchPayload) => {
    setIsLoading(true);
    setError(null);
    try {
      const response: SearchResponse = await searchApi.executeSearch(payload);
      setResults(response.results);
      setSearchPlan(response.search_plan);
      setSearchMode(response.search_mode);
      setTotalResults(response.total_results);
      setEmptySuggestion(response.empty_suggestion);
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

  return {
    query,
    setQuery,
    results,
    searchPlan,
    searchMode,
    totalResults,
    emptySuggestion,
    isLoading,
    error,
    execute,
  };
}
