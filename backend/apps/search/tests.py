from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Restaurant, MenuItem

class SearchPipelineAndApiTests(TestCase):
    def setUp(self):
        self.rest_sec62 = Restaurant.objects.create(
            name="Spice Haven Sector 62",
            locality="Sector 62",
            latitude=28.628,
            longitude=77.365,
            cuisines=["North Indian"],
            rating=4.6,
        )
        self.rest_sec18 = Restaurant.objects.create(
            name="Tandoor Club Sector 18",
            locality="Sector 18",
            latitude=28.570,
            longitude=77.326,
            cuisines=["North Indian"],
            rating=4.4,
        )
        # Dish 1: Spicy vegetarian paneer at ₹320 in Sector 62
        self.item_cheap_spicy_veg = MenuItem.objects.create(
            restaurant=self.rest_sec62,
            name="Kadhai Paneer Spicy",
            category="Main Course",
            price_paise=32000,
            ingredients=["paneer", "bell peppers", "onion"],
            dietary_tags=["vegetarian"],
            spice_level="spicy",
            allergen_info=["dairy"],
            is_available=True,
        )
        # Dish 2: Expensive paneer at ₹450 in Sector 62
        self.item_expensive = MenuItem.objects.create(
            restaurant=self.rest_sec62,
            name="Shahi Paneer Deluxe",
            category="Main Course",
            price_paise=45000,
            ingredients=["paneer", "cashew", "cream"],
            dietary_tags=["vegetarian"],
            spice_level="mild",
            allergen_info=["dairy", "nuts"],
            is_available=True,
        )
        # Dish 3: Jain Paneer in Sector 18 at ₹280
        self.item_jain = MenuItem.objects.create(
            restaurant=self.rest_sec18,
            name="Jain Paneer Masala (No Onion Garlic)",
            category="Main Course",
            price_paise=28000,
            ingredients=["paneer", "tomatoes", "curd"],
            dietary_tags=["vegetarian", "jain_friendly"],
            spice_level="medium",
            allergen_info=["dairy"],
            is_available=True,
        )

    def test_search_endpoint_with_natural_language_under_budget(self):
        url = reverse('search-execute')
        payload = {
            "query": "Show me spicy vegetarian dishes below ₹350 near Sector 62"
        }
        res = self.client.post(url, payload, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['search_mode'], 'fallback')
        self.assertEqual(data['search_plan']['max_price'], 350.0)
        self.assertIn("vegetarian", data['search_plan']['dietary_tags'])

        # Only the ₹320 dish should match; the ₹450 dish MUST NOT be returned!
        result_items = data['results']
        self.assertEqual(len(result_items), 1)
        self.assertEqual(result_items[0]['item']['name'], "Kadhai Paneer Spicy")
        self.assertTrue(any("budget" in r.lower() or "₹320" in r for r in result_items[0]['match_reasons']))

    def test_hard_dietary_constraints_strictly_enforced(self):
        url = reverse('search-execute')
        payload = {
            "query": "Jain food without onion and garlic"
        }
        res = self.client.post(url, payload, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        results = data['results']
        # Only item_jain satisfies jain_friendly
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['item']['name'], "Jain Paneer Masala (No Onion Garlic)")

    def test_search_suggestions_endpoint(self):
        url = reverse('search-suggestions')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.json()), 4)
