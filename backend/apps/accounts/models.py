from django.db import models
from django.contrib.auth.models import User
from apps.catalog.models import Restaurant, MenuItem

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorited_by'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                condition=models.Q(restaurant__isnull=False),
                name='unique_user_restaurant_favorite'
            ),
            models.UniqueConstraint(
                fields=['user', 'menu_item'],
                condition=models.Q(menu_item__isnull=False),
                name='unique_user_menu_item_favorite'
            ),
            models.CheckConstraint(
                check=models.Q(restaurant__isnull=False) | models.Q(menu_item__isnull=False),
                name='favorite_must_have_restaurant_or_menu_item'
            )
        ]

    def __str__(self):
        target = self.restaurant.name if self.restaurant else (self.menu_item.name if self.menu_item else "Unknown")
        return f"{self.user.username} favorited {target}"
