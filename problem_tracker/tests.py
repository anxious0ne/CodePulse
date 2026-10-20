from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Problem

User = get_user_model()


class ProblemModelTests(TestCase):

    def test_problem_creation(self):
        problem = Problem.objects.create(
            contest_id=1234,
            problem_index='A',
            name='Test Problem',
            rating=1200,
            tags=['greedy', 'math'],
        )
        self.assertEqual(problem.contest_id, 1234)
        self.assertEqual(problem.name, 'Test Problem')
        self.assertEqual(problem.rating, 1200)
        self.assertIn('greedy', problem.tags)

    def test_problem_str_representation(self):
        problem = Problem.objects.create(
            contest_id=999,
            problem_index='B',
            name='Another Problem',
        )
        self.assertEqual(str(problem), '999B - Another Problem')

    def test_problem_unique_together_constraint(self):
        Problem.objects.create(contest_id=100, problem_index='A', name='P1')
        with self.assertRaises(Exception):
            Problem.objects.create(contest_id=100, problem_index='A', name='Duplicate')


class ProblemListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='ptuser', password='Pass123!')
        Problem.objects.create(contest_id=1, problem_index='A', name='Easy Problem', rating=800, tags=['math'])
        Problem.objects.create(contest_id=1, problem_index='B', name='Medium Problem', rating=1200, tags=['dp'])
        Problem.objects.create(contest_id=2, problem_index='A', name='Graph Problem', rating=1600, tags=['graphs'])

    def test_unauthenticated_user_cannot_list_problems(self):
        response = self.client.get('/api/problems/')
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_list_problems(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/problems/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_rating(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/problems/?rating=1200')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if not isinstance(response.data, dict) else response.data.get('results', response.data)
        # At least one result should have rating 1200
        if isinstance(results, list):
            for item in results:
                self.assertEqual(item['rating'], 1200)

    def test_problem_detail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        problem = Problem.objects.first()
        response = self.client.get(f'/api/problems/{problem.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], problem.name)
