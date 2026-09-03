from typing import Optional
from django.db.models import QuerySet
from .models import Restaurant, MenuItem

def get_filtered_restaurants(
    locality: Optional[str] = None,
    cuisine: Optional[str] = None,
    price_band: Optional[str] = None,
    min_rating: Optional[float] = None,
) -> QuerySet[Restaurant]:
    """Return filtered queryset of restaurants."""
    qs = Restaurant.objects.all().prefetch_related('menu_items')
    if locality:
        qs = qs.filter(locality__iexact=locality)
    if cuisine:
        # Cuisines is a JSON list of strings
        qs = qs.filter(cuisines__icontains=cuisine)
    if price_band:
        qs = qs.filter(price_band=price_band)
    if min_rating:
        qs = qs.filter(rating__gte=min_rating)
    return qs

def get_filtered_menu_items(
    restaurant_id: Optional[int] = None,
    category: Optional[str] = None,
    max_price_paise: Optional[int] = None,
    dietary_tag: Optional[str] = None,
    spice_level: Optional[str] = None,
) -> QuerySet[MenuItem]:
    """Return filtered queryset of menu items."""
    qs = MenuItem.objects.select_related('restaurant').all()
    if restaurant_id:
        qs = qs.filter(restaurant_id=restaurant_id)
    if category:
        qs = qs.filter(category__iexact=category)
    if max_price_paise:
        qs = qs.filter(price_paise__lte=max_price_paise)
    if dietary_tag:
        qs = qs.filter(dietary_tags__icontains=dietary_tag)
    if spice_level:
        qs = qs.filter(spice_level=spice_level)
    return qs
