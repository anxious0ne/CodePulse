from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_page_get_returns_200(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_register_with_valid_data_creates_user(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_with_valid_data_redirects(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })
        self.assertIn(response.status_code, [301, 302])

    def test_register_with_mismatched_passwords_fails(self):
        response = self.client.post(self.register_url, {
            'username': 'baduser',
            'email': 'bad@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'WrongPass456',
        })
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_register_with_existing_username_fails(self):
        User.objects.create_user(username='existing', password='Pass123!')
        response = self.client.post(self.register_url, {
            'username': 'existing',
            'email': 'another@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
        })
        self.assertEqual(User.objects.filter(username='existing').count(), 1)


class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='loginuser',
            password='TestPass123!'
        )

    def test_login_page_get_returns_200(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials_redirects(self):
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'TestPass123!',
        })
        self.assertIn(response.status_code, [301, 302])

    def test_login_with_invalid_credentials_stays_on_page(self):
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_with_nonexistent_user_fails(self):
        response = self.client.post(self.login_url, {
            'username': 'nobody',
            'password': 'SomePass123!',
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='logoutuser',
            password='TestPass123!'
        )

    def test_logout_redirects_to_login(self):
        self.client.login(username='logoutuser', password='TestPass123!')
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [301, 302])


class DashboardProtectionTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_unauthenticated_user_cannot_access_dashboard(self):
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [301, 302])
        self.assertIn('login', response['Location'].lower())
