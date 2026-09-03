from typing import Optional
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from .models import Favorite
from apps.catalog.models import Restaurant, MenuItem

def get_user_favorites(user: User):
    """Retrieve all favorites belonging strictly to the authenticated user."""
    return Favorite.objects.filter(user=user).select_related('restaurant', 'menu_item', 'menu_item__restaurant')

def toggle_favorite(
    user: User,
    restaurant_id: Optional[int] = None,
    menu_item_id: Optional[int] = None
) -> tuple[Optional[Favorite], bool]:
    """
    Toggles a favorite. If it exists, it is deleted and returns (None, False).
    If it does not exist, it is created and returns (favorite, True).
    """
    if restaurant_id:
        existing = Favorite.objects.filter(user=user, restaurant_id=restaurant_id).first()
        if existing:
            existing.delete()
            return None, False
        fav = Favorite.objects.create(user=user, restaurant_id=restaurant_id)
        return fav, True

    if menu_item_id:
        existing = Favorite.objects.filter(user=user, menu_item_id=menu_item_id).first()
        if existing:
            existing.delete()
            return None, False
        fav = Favorite.objects.create(user=user, menu_item_id=menu_item_id)
        return fav, True

    raise ValidationError("Must supply either restaurant_id or menu_item_id.")

def delete_user_favorite(user: User, favorite_id: int) -> bool:
    """Safely delete favorite ensuring ownership."""
    fav = Favorite.objects.filter(id=favorite_id).first()
    if not fav:
        return False
    if fav.user != user:
        raise PermissionDenied("You do not have permission to delete this favorite.")
    fav.delete()
    return True
