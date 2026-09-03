from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from apps.catalog.models import Restaurant
from apps.accounts.models import Favorite

class AccountsAndFavoritesTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='Password123!', email='u1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='Password123!', email='u2@example.com')
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            locality="Sector 18",
            latitude=28.57,
            longitude=77.32,
            cuisines=["Italian"],
            price_band="₹₹",
            rating=4.5,
        )

    def test_register_and_login_flow(self):
        # Register new user
        register_url = reverse('auth-register')
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!',
        }
        res = self.client.post(register_url, payload, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['username'], 'newuser')

        # Check me endpoint while logged in
        me_url = reverse('auth-me')
        me_res = self.client.get(me_url)
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()['username'], 'newuser')

        # Logout
        logout_url = reverse('auth-logout')
        logout_res = self.client.post(logout_url)
        self.assertEqual(logout_res.status_code, 200)

        # Me endpoint after logout should return 401
        me_after_res = self.client.get(me_url)
        self.assertEqual(me_after_res.status_code, 401)

    def test_favorites_cross_user_isolation(self):
        # Create favorite for user1
        fav1 = Favorite.objects.create(user=self.user1, restaurant=self.restaurant)

        # Login as user2
        self.client.login(username='user2', password='Password123!')

        # User2 lists favorites -> user1's favorite must NOT appear
        fav_url = reverse('favorite-list')
        list_res = self.client.get(fav_url)
        self.assertEqual(list_res.status_code, 200)
        self.assertEqual(len(list_res.json()), 0)

        # User2 tries to delete user1's favorite -> must be forbidden
        del_url = reverse('favorite-detail', kwargs={'pk': fav1.id})
        del_res = self.client.delete(del_url)
        self.assertEqual(del_res.status_code, 403)
        self.assertTrue(Favorite.objects.filter(id=fav1.id).exists())

        # User2 adds favorite
        add_res = self.client.post(fav_url, {'restaurant': self.restaurant.id}, content_type='application/json')
        self.assertEqual(add_res.status_code, 201)
        self.assertTrue(Favorite.objects.filter(user=self.user2, restaurant=self.restaurant).exists())
