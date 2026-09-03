from django.test import TestCase
from django.urls import reverse

class HealthCheckTest(TestCase):
    def test_health_check_returns_200_and_expected_structure(self):
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['checks']['database'])
        self.assertIn('duration_ms', data)
