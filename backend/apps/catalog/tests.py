from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from apps.catalog.models import Restaurant, MenuItem

class CatalogModelsAndViewsTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Royal Tadka",
            locality="Sector 62",
            address="Plot 12, Sector 62",
            latitude=28.628,
            longitude=77.365,
            cuisines=["North Indian"],
            price_band="₹₹",
            rating=4.5,
            review_count=120,
            is_demo=True,
        )
        self.item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Paneer Butter Masala",
            category="Main Course",
            price_paise=32000,
            ingredients=["paneer", "butter", "tomatoes"],
            dietary_tags=["vegetarian"],
            spice_level="mild",
            allergen_info=["dairy"],
            is_available=True,
            is_demo=True,
        )
        self.item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Palak Corn",
            category="Main Course",
            price_paise=26000,
            ingredients=["spinach", "corn"],
            dietary_tags=["vegetarian", "vegan", "gluten_free"],
            spice_level="medium",
            allergen_info=[],
            is_available=True,
            is_demo=True,
        )

    def test_restaurant_list_and_filter(self):
        url = reverse('restaurant-list')
        response = self.client.get(url, {'locality': 'Sector 62'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        results = data.get('results', data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Test Royal Tadka")

    def test_restaurant_detail(self):
        url = reverse('restaurant-detail', kwargs={'slug': self.restaurant.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "Test Royal Tadka")
        self.assertEqual(len(data['menu_items']), 2)

    def test_menu_items_price_and_dietary_filter(self):
        url = reverse('menu-item-list')
        # Filter max price ₹300 (should return only Palak Corn at ₹260)
        response = self.client.get(url, {'max_price': 300, 'dietary_tag': 'vegan'})
        self.assertEqual(response.status_code, 200)
        results = response.json().get('results', [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Palak Corn")

    def test_seed_demo_data_command(self):
        # Call seed demo data command
        call_command('seed_demo_data')
        self.assertGreaterEqual(Restaurant.objects.count(), 50)
        self.assertGreaterEqual(MenuItem.objects.count(), 500)
        
        # Calling again without reset shouldn't double records (idempotent)
        count_before = Restaurant.objects.count()
        call_command('seed_demo_data')
        self.assertEqual(Restaurant.objects.count(), count_before)
