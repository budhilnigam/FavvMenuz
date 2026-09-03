from rest_framework import serializers
from .models import Restaurant, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    price_inr = serializers.FloatField(read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant_slug = serializers.CharField(source='restaurant.slug', read_only=True)
    restaurant_locality = serializers.CharField(source='restaurant.locality', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'restaurant',
            'restaurant_name',
            'restaurant_slug',
            'restaurant_locality',
            'name',
            'slug',
            'category',
            'description',
            'price_paise',
            'price_inr',
            'ingredients',
            'dietary_tags',
            'spice_level',
            'allergen_info',
            'image_asset',
            'is_available',
            'is_demo',
            'created_at',
        ]
        read_only_fields = ['id', 'is_demo', 'created_at']


class RestaurantSerializer(serializers.ModelSerializer):
    menu_items_count = serializers.IntegerField(source='menu_items.count', read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'cuisines',
            'locality',
            'address',
            'latitude',
            'longitude',
            'price_band',
            'rating',
            'review_count',
            'image_asset',
            'is_demo',
            'menu_items_count',
            'created_at',
        ]
        read_only_fields = ['id', 'slug', 'is_demo', 'created_at']


class RestaurantDetailSerializer(RestaurantSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta(RestaurantSerializer.Meta):
        fields = RestaurantSerializer.Meta.fields + ['menu_items']
