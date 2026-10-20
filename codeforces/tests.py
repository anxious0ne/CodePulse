from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

User = get_user_model()


class CodeforcesConnectTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='cfuser', password='Pass123!')

    def test_unauthenticated_cannot_connect(self):
        response = self.client.post('/api/codeforces/connect/', {'handle': 'tourist'}, format='json')
        self.assertIn(response.status_code, [401, 403])

    def test_connect_with_valid_handle(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/codeforces/connect/', {'handle': 'tourist'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.codeforces_handle, 'tourist')

    def test_connect_with_empty_handle_returns_error(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/codeforces/connect/', {'handle': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_connect_without_handle_field_returns_error(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/codeforces/connect/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CodeforcesStatusTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='statususer', password='Pass123!')

    def test_unauthenticated_cannot_get_status(self):
        response = self.client.get('/api/codeforces/status/')
        self.assertIn(response.status_code, [401, 403])

    def test_status_without_handle(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/codeforces/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['connected'])
        self.assertIsNone(response.data['handle'])

    def test_status_with_handle(self):
        self.user.codeforces_handle = 'tourist'
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/codeforces/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['connected'])
        self.assertEqual(response.data['handle'], 'tourist')


class CodeforcesServiceUnitTests(TestCase):

    def test_get_cf_rank_info_newbie(self):
        from .services import get_cf_rank_info
        info = get_cf_rank_info(1100)
        self.assertEqual(info['title'], 'Newbie')
        self.assertEqual(info['color'], '#9ca3af')

    def test_get_cf_rank_info_expert(self):
        from .services import get_cf_rank_info
        info = get_cf_rank_info(1750)
        self.assertEqual(info['title'], 'Expert')
        self.assertEqual(info['color'], '#3b82f6')

    def test_get_cf_rank_info_grandmaster(self):
        from .services import get_cf_rank_info
        info = get_cf_rank_info(2450)
        self.assertEqual(info['title'], 'Grandmaster')
        self.assertEqual(info['color'], '#ef4444')

    def test_get_cf_rank_info_unrated(self):
        from .services import get_cf_rank_info
        info = get_cf_rank_info(None)
        self.assertEqual(info['title'], 'Unrated')
        self.assertEqual(info['color'], '#94a3b8')
