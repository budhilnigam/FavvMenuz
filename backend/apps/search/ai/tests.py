from django.test import TestCase
from apps.search.ai.schemas import SearchPlan
from apps.search.ai.parser import parse_query_fallback
from apps.search.ai.provider import LLMProvider

class AIInterpretationTests(TestCase):
    def test_fallback_parser_price_and_dietary(self):
        query = "Show me spicy vegetarian dishes below ₹350 near Sector 62"
        plan = parse_query_fallback(query)
        self.assertEqual(plan.max_price, 350.0)
        self.assertIn("vegetarian", plan.dietary_tags)
        self.assertEqual(plan.spice_level, "spicy")
        self.assertEqual(plan.locality, "Sector 62")

    def test_fallback_parser_jain_and_distance(self):
        query = "Show me Jain-friendly dinner options within 3 km of Sector 137"
        plan = parse_query_fallback(query)
        self.assertIn("jain_friendly", plan.dietary_tags)
        self.assertIn("vegetarian", plan.dietary_tags)
        self.assertIn("onion", plan.excluded_ingredients)
        self.assertIn("garlic", plan.excluded_ingredients)
        self.assertEqual(plan.max_distance_km, 3.0)
        self.assertEqual(plan.locality, "Sector 137")

    def test_fallback_parser_excluded_ingredient(self):
        query = "Find dishes without peanuts under 500"
        plan = parse_query_fallback(query)
        self.assertIn("peanuts", plan.excluded_ingredients)
        self.assertEqual(plan.max_price, 500.0)

    def test_llm_provider_unconfigured_graceful_fallback(self):
        # With default empty LLM_API_KEY, provider should gracefully return None
        provider = LLMProvider()
        provider.api_key = ""
        result = provider.parse_query("Find paneer tikka")
        self.assertIsNone(result)
