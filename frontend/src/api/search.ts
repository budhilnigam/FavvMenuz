import { apiClient } from './client';
import { SearchResponse, SearchSuggestion } from '../types/search';

export interface SearchPayload {
  query?: string;
  locality?: string | null;
  cuisines?: string[];
  dietary_tags?: string[];
  max_price?: number | null;
  min_price?: number | null;
  spice_level?: string | null;
  max_distance_km?: number | null;
  sort_by?: string;
}

export const searchApi = {
  executeSearch: async (payload: SearchPayload): Promise<SearchResponse> => {
    return apiClient<SearchResponse>('/api/search/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  getSuggestions: async (): Promise<SearchSuggestion[]> => {
    return apiClient<SearchSuggestion[]>('/api/search/suggestions/');
  },
};
