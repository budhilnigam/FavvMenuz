import { apiClient } from './client';
import { Restaurant, MenuItem } from '../types/restaurant';
import { PaginatedResponse } from '../types/api';

export interface RestaurantFilters {
  locality?: string;
  cuisine?: string;
  price_band?: string;
  min_rating?: number;
  search?: string;
  ordering?: string;
  page?: number;
}

export const restaurantsApi = {
  list: async (filters: RestaurantFilters = {}): Promise<PaginatedResponse<Restaurant>> => {
    const params = new URLSearchParams();
    if (filters.locality) params.append('locality', filters.locality);
    if (filters.cuisine) params.append('cuisine', filters.cuisine);
    if (filters.price_band) params.append('price_band', filters.price_band);
    if (filters.min_rating) params.append('min_rating', String(filters.min_rating));
    if (filters.search) params.append('search', filters.search);
    if (filters.ordering) params.append('ordering', filters.ordering);
    if (filters.page) params.append('page', String(filters.page));

    const queryStr = params.toString() ? `?${params.toString()}` : '';
    return apiClient<PaginatedResponse<Restaurant>>(`/api/restaurants/${queryStr}`);
  },

  getDetail: async (slug: string): Promise<Restaurant> => {
    return apiClient<Restaurant>(`/api/restaurants/${slug}/`);
  },

  listMenuItems: async (params: {
    restaurant_id?: number;
    category?: string;
    max_price?: number;
    dietary_tag?: string;
    spice_level?: string;
    search?: string;
    page?: number;
  } = {}): Promise<PaginatedResponse<MenuItem>> => {
    const qp = new URLSearchParams();
    if (params.restaurant_id) qp.append('restaurant_id', String(params.restaurant_id));
    if (params.category) qp.append('category', params.category);
    if (params.max_price) qp.append('max_price', String(params.max_price));
    if (params.dietary_tag) qp.append('dietary_tag', params.dietary_tag);
    if (params.spice_level) qp.append('spice_level', params.spice_level);
    if (params.search) qp.append('search', params.search);
    if (params.page) qp.append('page', String(params.page));

    const qs = qp.toString() ? `?${qp.toString()}` : '';
    return apiClient<PaginatedResponse<MenuItem>>(`/api/menu-items/${qs}`);
  },
};
