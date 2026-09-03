import { apiClient } from './client';
import { FavoriteItem } from '../types/restaurant';

export const favoritesApi = {
  list: async (): Promise<FavoriteItem[]> => {
    return apiClient<FavoriteItem[]>('/api/favorites/');
  },

  toggle: async (payload: { restaurant?: number; menu_item?: number }): Promise<{ detail: string; favorited: boolean; favorite?: FavoriteItem }> => {
    return apiClient<{ detail: string; favorited: boolean; favorite?: FavoriteItem }>('/api/favorites/', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  remove: async (id: number): Promise<void> => {
    return apiClient<void>(`/api/favorites/${id}/`, {
      method: 'DELETE',
    });
  },
};
