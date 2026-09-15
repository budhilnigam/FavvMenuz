"""
FavvMenuz URL Configuration
"""
from django.urls import path, include
from apps.core.views import health_check

urlpatterns = [
    # Health and readiness endpoint
    path('healthz/', health_check, name='health-check'),

    # Django Admin

    # Authentication & User Management
    path('api/auth/', include('apps.accounts.urls')),

    # Restaurants and Menu Catalog
    path('api/', include('apps.catalog.urls')),

    # Natural-Language and Structured Search
    path('api/search/', include('apps.search.urls')),

    # User Favorites
    path('api/favorites/', include('apps.accounts.favorites_urls')),
]
