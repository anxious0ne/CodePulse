from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

User = get_user_model()


class ProfileModelTests(TestCase):

    def test_profile_auto_created_on_user_creation(self):
        user = User.objects.create_user(username='profuser', password='Pass123!')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str_representation(self):
        user = User.objects.create_user(username='struser', password='Pass123!')
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(profile), 'Profile of struser')


class ProfileViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='viewuser', password='Pass123!')

    def test_unauthenticated_cannot_access_profile(self):
        response = self.client.get('/api/profile/')
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_gets_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'viewuser')

    def test_update_profile_bio(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/profile/', {'bio': 'I love coding!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'I love coding!')

    def test_update_profile_github(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/profile/', {'github_username': 'mygh'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['github_username'], 'mygh')
