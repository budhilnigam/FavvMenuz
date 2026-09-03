from django.contrib import admin
from .models import Restaurant, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'category', 'price_paise', 'spice_level', 'is_available')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'locality', 'price_band', 'rating', 'review_count', 'is_demo')
    list_filter = ('locality', 'price_band', 'is_demo')
    search_fields = ('name', 'locality', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price_inr', 'spice_level', 'is_available')
    list_filter = ('category', 'spice_level', 'is_available', 'is_demo')
    search_fields = ('name', 'description', 'restaurant__name')
    list_select_related = ('restaurant',)
