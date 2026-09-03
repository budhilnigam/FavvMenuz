from django.urls import path
from .views import SearchView, SearchSuggestionsView

urlpatterns = [
    path('', SearchView.as_view(), name='search-execute'),
    path('suggestions/', SearchSuggestionsView.as_view(), name='search-suggestions'),
]
