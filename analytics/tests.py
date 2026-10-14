from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from problem_tracker.models import Problem
from submissions.models import Submission

User = get_user_model()


class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='analyst', password='password123')
        self.client.login(username='analyst', password='password123')

        p1 = Problem.objects.create(contest_id=1001, problem_index='A', name='P1', rating=900, tags=['dp', 'math'])
        p2 = Problem.objects.create(contest_id=1001, problem_index='B', name='P2', rating=1500, tags=['dp'])

        Submission.objects.create(user=self.user, problem=p1, verdict='OK', language='C++', submitted_at=timezone.now())
        Submission.objects.create(user=self.user, problem=p2, verdict='WRONG_ANSWER', language='C++', submitted_at=timezone.now())

    def test_topic_analytics(self):
        res = self.client.get(reverse('api-analytics-topics'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        dp_stat = next((item for item in data if item['tag'] == 'dp'), None)
        self.assertIsNotNone(dp_stat)
        self.assertEqual(dp_stat['attempted'], 2)
        self.assertEqual(dp_stat['solved'], 1)
        self.assertEqual(dp_stat['solve_rate'], 0.5)

    def test_verdict_analytics(self):
        res = self.client.get(reverse('api-analytics-verdicts'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['total'], 2)
        breakdown = {b['key']: b['count'] for b in data['breakdown']}
        self.assertEqual(breakdown.get('OK'), 1)
        self.assertEqual(breakdown.get('WRONG_ANSWER'), 1)

    def test_rating_distribution(self):
        res = self.client.get(reverse('api-analytics-ratings'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        under_1000 = next((item for item in data if item['range'] == '< 1000'), None)
        self.assertIsNotNone(under_1000)
        self.assertEqual(under_1000['count'], 1)
