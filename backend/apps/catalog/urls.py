from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, MenuItemListView

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('menu-items/', MenuItemListView.as_view(), name='menu-item-list'),
]
