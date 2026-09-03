import { useState, useEffect, useCallback } from 'react';
import { FavoriteItem } from '../types/restaurant';
import { favoritesApi } from '../api/favorites';
import { useAuth } from './useAuth';

export function useFavorites() {
  const { user } = useAuth();
  const [favorites, setFavorites] = useState<FavoriteItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchFavorites = useCallback(async () => {
    if (!user) {
      setFavorites([]);
      return;
    }
    setIsLoading(true);
    try {
      const items = await favoritesApi.list();
      setFavorites(items);
    } catch (err) {
      console.warn('Failed to fetch favorites:', err);
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchFavorites();
  }, [fetchFavorites]);

  const isFavorited = (restaurantId?: number, menuItemId?: number): boolean => {
    if (restaurantId) {
      return favorites.some((f) => f.restaurant === restaurantId);
    }
    if (menuItemId) {
      return favorites.some((f) => f.menu_item === menuItemId);
    }
    return false;
  };

  const getFavoriteId = (restaurantId?: number, menuItemId?: number): number | undefined => {
    if (restaurantId) {
      return favorites.find((f) => f.restaurant === restaurantId)?.id;
    }
    if (menuItemId) {
      return favorites.find((f) => f.menu_item === menuItemId)?.id;
    }
    return undefined;
  };

  const toggleFavorite = async (restaurantId?: number, menuItemId?: number): Promise<boolean> => {
    if (!user) {
      throw new Error('Please login to save favorites.');
    }
    const res = await favoritesApi.toggle({
      restaurant: restaurantId,
      menu_item: menuItemId,
    });
    await fetchFavorites();
    return res.favorited;
  };

  const removeFavorite = async (favoriteId: number): Promise<void> => {
    await favoritesApi.remove(favoriteId);
    setFavorites((prev) => prev.filter((f) => f.id !== favoriteId));
  };

  return {
    favorites,
    isLoading,
    isFavorited,
    getFavoriteId,
    toggleFavorite,
    removeFavorite,
    refetch: fetchFavorites,
  };
}
