from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, RestaurantDetailSerializer, MenuItemSerializer
from .services import get_filtered_restaurants, get_filtered_menu_items

class RestaurantListView(generics.ListAPIView):
    """
    List restaurants with filtering by locality, cuisine, price band, and min rating.
    """
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'locality', 'description']
    ordering_fields = ['rating', 'review_count', 'name', 'created_at']
    ordering = ['-rating']

    def get_queryset(self):
        locality = self.request.query_params.get('locality')
        cuisine = self.request.query_params.get('cuisine')
        price_band = self.request.query_params.get('price_band')
        min_rating_raw = self.request.query_params.get('min_rating')

        min_rating = None
        if min_rating_raw:
            try:
                min_rating = float(min_rating_raw)
            except ValueError:
                pass

        return get_filtered_restaurants(
            locality=locality,
            cuisine=cuisine,
            price_band=price_band,
            min_rating=min_rating
        )


class RestaurantDetailView(generics.RetrieveAPIView):
    """
    Retrieve single restaurant details by slug, including full menu items.
    """
    queryset = Restaurant.objects.all().prefetch_related('menu_items')
    serializer_class = RestaurantDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class MenuItemListView(generics.ListAPIView):
    """
    List menu items with pagination and deterministic filters.
    """
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['price_paise', 'name', 'created_at']
    ordering = ['category', 'price_paise']

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        category = self.request.query_params.get('category')
        max_price_raw = self.request.query_params.get('max_price')
        dietary_tag = self.request.query_params.get('dietary_tag')
        spice_level = self.request.query_params.get('spice_level')

        max_price_paise = None
        if max_price_raw:
            try:
                # If passed in rupees, convert to paise
                max_price_paise = int(float(max_price_raw) * 100)
            except ValueError:
                pass

        return get_filtered_menu_items(
            restaurant_id=int(restaurant_id) if restaurant_id and restaurant_id.isdigit() else None,
            category=category,
            max_price_paise=max_price_paise,
            dietary_tag=dietary_tag,
            spice_level=spice_level
        )
