from django.db import models
from django.utils.text import slugify

class Restaurant(models.Model):
    PRICE_BAND_CHOICES = [
        ('₹', 'Budget (Under ₹300)'),
        ('₹₹', 'Moderate (₹300 - ₹700)'),
        ('₹₹₹', 'Premium (₹700 - ₹1500)'),
        ('₹₹₹₹', 'Fine Dining (₹1500+)'),
    ]

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    description = models.TextField(blank=True)
    cuisines = models.JSONField(default=list, help_text="List of cuisine names, e.g. ['North Indian', 'Mughlai']")
    locality = models.CharField(max_length=150, db_index=True)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    price_band = models.CharField(max_length=8, choices=PRICE_BAND_CHOICES, default='₹₹')
    rating = models.FloatField(default=4.0, db_index=True)
    review_count = models.PositiveIntegerField(default=100)
    image_asset = models.CharField(max_length=200, default='restaurant_default')
    is_demo = models.BooleanField(default=True, help_text="Always True for synthetic demo data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating', 'name']
        indexes = [
            models.Index(fields=['locality', 'rating']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Restaurant.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.locality})"


class MenuItem(models.Model):
    SPICE_LEVEL_CHOICES = [
        ('none', 'Not Spicy'),
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('spicy', 'Spicy'),
        ('extra_spicy', 'Extra Spicy'),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, blank=True)
    category = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price_paise = models.PositiveIntegerField(
        help_text="Price in paise (e.g. 35000 = ₹350.00)",
        db_index=True
    )
    ingredients = models.JSONField(
        default=list,
        help_text="List of ingredients, e.g. ['paneer', 'capsicum', 'onion', 'yogurt']"
    )
    dietary_tags = models.JSONField(
        default=list,
        help_text="List of dietary tags: ['vegetarian', 'vegan', 'jain_friendly', 'dairy_free', 'gluten_free']"
    )
    spice_level = models.CharField(
        max_length=20,
        choices=SPICE_LEVEL_CHOICES,
        default='medium',
        db_index=True
    )
    allergen_info = models.JSONField(
        default=list,
        help_text="Known allergens, e.g. ['dairy', 'nuts', 'gluten']"
    )
    image_asset = models.CharField(max_length=200, default='dish_default')
    is_available = models.BooleanField(
        default=True,
        help_text="Simulated availability status for demo"
    )
    is_demo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'price_paise', 'name']
        indexes = [
            models.Index(fields=['price_paise', 'spice_level']),
            models.Index(fields=['restaurant', 'category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def price_inr(self) -> float:
        return self.price_paise / 100.0

    def __str__(self):
        return f"{self.name} - ₹{self.price_inr:.2f} ({self.restaurant.name})"
