from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.services import get_cf_rank_info

User = get_user_model()


class UserModelAndServicesTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testcoder',
            email='test@example.com',
            password='Password123!',
            codeforces_handle='test_cf_handle'
        )
        self.assertEqual(user.username, 'testcoder')
        self.assertEqual(user.codeforces_handle, 'test_cf_handle')
        self.assertFalse(user.is_handle_verified)

    def test_get_cf_rank_info(self):
        self.assertEqual(get_cf_rank_info(None)['title'], 'Unrated')
        self.assertEqual(get_cf_rank_info(1100)['title'], 'Newbie')
        self.assertEqual(get_cf_rank_info(1350)['title'], 'Pupil')
        self.assertEqual(get_cf_rank_info(1550)['title'], 'Specialist')
        self.assertEqual(get_cf_rank_info(1750)['title'], 'Expert')
        self.assertEqual(get_cf_rank_info(2000)['title'], 'Candidate Master')
        self.assertEqual(get_cf_rank_info(2200)['title'], 'Master')
        self.assertEqual(get_cf_rank_info(2500)['title'], 'Grandmaster')
        self.assertEqual(get_cf_rank_info(3200)['title'], 'Legendary Grandmaster')


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_and_login_flow(self):
        # Register
        res = self.client.post(reverse('register-direct'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'secretpassword',
            'confirm_password': 'secretpassword',
            'codeforces_handle': 'newuser_cf'
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Logout
        res_logout = self.client.get(reverse('logout-direct'), follow=True)
        self.assertEqual(res_logout.status_code, 200)

        # Login
        res_login = self.client.post(reverse('login-direct'), {
            'username': 'newuser',
            'password': 'secretpassword'
        }, follow=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)


class DashboardSummaryApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='apicoder',
            password='secretpassword',
            codeforces_handle='apicoder_cf'
        )

    def test_unauthenticated_access_denied(self):
        res = self.client.get(reverse('api-dashboard'))
        self.assertEqual(res.status_code, 403)

    def test_authenticated_summary(self):
        self.client.login(username='apicoder', password='secretpassword')
        res = self.client.get(reverse('api-dashboard'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['username'], 'apicoder')
        self.assertEqual(data['codeforces_handle'], 'apicoder_cf')
        self.assertEqual(data['total_submissions'], 0)
