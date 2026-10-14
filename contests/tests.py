from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from contests.models import Contest
from contests.serializers import ContestSerializer

User = get_user_model()


class ContestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='contestant', password='password123')
        self.contest = Contest.objects.create(
            user=self.user,
            contest_id=1900,
            contest_name='Codeforces Round 950 (Div. 2)',
            rank=450,
            old_rating=1420,
            new_rating=1510,
            rating_update_time=timezone.now()
        )

    def test_contest_serializer_delta(self):
        serializer = ContestSerializer(self.contest)
        data = serializer.data
        self.assertEqual(data['delta'], 90)
        self.assertEqual(data['new_rating'], 1510)

    def test_contest_list_view(self):
        self.client.login(username='contestant', password='password123')
        res = self.client.get(reverse('api-contests'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['contest_id'], 1900)
        self.assertEqual(data[0]['delta'], 90)
