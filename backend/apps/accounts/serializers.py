from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Favorite
from apps.catalog.serializers import RestaurantSerializer, MenuItemSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields did not match."})
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    restaurant_details = RestaurantSerializer(source='restaurant', read_only=True)
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'id',
            'restaurant',
            'restaurant_details',
            'menu_item',
            'menu_item_details',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        restaurant = attrs.get('restaurant')
        menu_item = attrs.get('menu_item')
        if not restaurant and not menu_item:
            raise serializers.ValidationError("Either restaurant or menu_item must be provided.")
        if restaurant and menu_item:
            raise serializers.ValidationError("Specify either restaurant or menu_item, not both in a single favorite.")
        return attrs
