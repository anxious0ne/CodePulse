from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from problem_tracker.models import Problem
from submissions.models import Submission

User = get_user_model()


class SubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='solver', password='password123')
        self.problem = Problem.objects.create(
            contest_id=1900,
            problem_index='A',
            name='Cover in Water',
            rating=800,
            tags=['greedy', 'implementation']
        )
        self.sub1 = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            verdict='OK',
            language='GNU C++20',
            submitted_at=timezone.now()
        )
        self.sub2 = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            verdict='WRONG_ANSWER',
            language='Python 3',
            submitted_at=timezone.now()
        )

    def test_recent_submissions_view(self):
        self.client.login(username='solver', password='password123')
        res = self.client.get(reverse('api-submissions-recent'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 2)

    def test_filter_by_verdict(self):
        self.client.login(username='solver', password='password123')
        res = self.client.get(reverse('api-submissions-recent') + '?verdict=OK')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['verdict'], 'OK')
        self.assertEqual(data[0]['problem_name'], 'Cover in Water')
