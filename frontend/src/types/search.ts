import { MenuItem, Restaurant } from './restaurant';

export interface SearchPlan {
  query_text: string;
  keywords: string[];
  cuisines: string[];
  included_ingredients: string[];
  excluded_ingredients: string[];
  dietary_tags: string[];
  min_price: number | null;
  max_price: number | null;
  spice_level: string | null;
  locality: string | null;
  max_distance_km: number | null;
  sort_by: string;
}

export interface SearchResultItem {
  item: MenuItem;
  restaurant: Restaurant;
  relevance_score: number;
  match_reasons: string[];
  distance_km: number | null;
}

export interface SearchResponse {
  search_plan: SearchPlan;
  search_mode: 'ai' | 'fallback';
  total_results: number;
  results: SearchResultItem[];
  empty_suggestion: string | null;
  is_demo_data: boolean;
}

export interface SearchSuggestion {
  id: string;
  label: string;
  query: string;
  badge: string;
  icon: string;
}
