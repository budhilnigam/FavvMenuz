export interface Restaurant {
  id: number;
  name: string;
  slug: string;
  description: string;
  cuisines: string[];
  locality: string;
  address: string;
  latitude: number;
  longitude: number;
  price_band: string;
  rating: number;
  review_count: number;
  image_asset: string;
  is_demo: boolean;
  menu_items_count?: number;
  menu_items?: MenuItem[];
  created_at: string;
}

export interface MenuItem {
  id: number;
  restaurant: number;
  restaurant_name?: string;
  restaurant_slug?: string;
  restaurant_locality?: string;
  name: string;
  slug: string;
  category: string;
  description: string;
  price_paise: number;
  price_inr: number;
  ingredients: string[];
  dietary_tags: string[];
  spice_level: 'none' | 'mild' | 'medium' | 'spicy' | 'extra_spicy';
  allergen_info: string[];
  image_asset: string;
  is_available: boolean;
  is_demo: boolean;
  created_at: string;
}

export interface FavoriteItem {
  id: number;
  restaurant?: number | null;
  restaurant_details?: Restaurant | null;
  menu_item?: number | null;
  menu_item_details?: MenuItem | null;
  created_at: string;
}
