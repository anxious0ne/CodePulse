from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Goal

User = get_user_model()


class GoalModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='goaluser', password='Pass123!')

    def test_goal_creation(self):
        goal = Goal.objects.create(
            user=self.user,
            title='Solve 100 problems',
            goal_type='problems_solved',
            target_value=100,
            current_value=32,
        )
        self.assertEqual(goal.title, 'Solve 100 problems')
        self.assertEqual(goal.target_value, 100)
        self.assertFalse(goal.is_completed)

    def test_goal_str_representation(self):
        goal = Goal.objects.create(user=self.user, title='My Goal', target_value=50)
        self.assertEqual(str(goal), 'goaluser: My Goal')

    def test_progress_percentage_calculation(self):
        goal = Goal.objects.create(
            user=self.user, title='Test', target_value=100, current_value=64
        )
        self.assertEqual(goal.progress_percentage, 64)

    def test_progress_percentage_capped_at_100(self):
        goal = Goal.objects.create(
            user=self.user, title='Overflow', target_value=10, current_value=150
        )
        self.assertEqual(goal.progress_percentage, 100)

    def test_progress_percentage_zero_target(self):
        goal = Goal.objects.create(user=self.user, title='Zero', target_value=0)
        self.assertEqual(goal.progress_percentage, 0)


class GoalAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apigoaluser', password='Pass123!')
        self.other_user = User.objects.create_user(username='othergoaluser', password='Pass123!')

    def test_unauthenticated_cannot_list_goals(self):
        response = self.client.get('/api/goals/')
        self.assertIn(response.status_code, [401, 403])

    def test_create_goal(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/goals/', {
            'title': 'Reach 1500 rating',
            'goal_type': 'rating',
            'target_value': 1500,
            'current_value': 1200,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.filter(user=self.user).count(), 1)

    def test_list_only_own_goals(self):
        Goal.objects.create(user=self.user, title='My Goal', target_value=10)
        Goal.objects.create(user=self.other_user, title='Other Goal', target_value=20)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/goals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', [])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'My Goal')

    def test_update_goal_current_value(self):
        goal = Goal.objects.create(user=self.user, title='Update Me', target_value=50, current_value=10)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/goals/{goal.id}/', {'current_value': 25}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.current_value, 25)

    def test_delete_goal(self):
        goal = Goal.objects.create(user=self.user, title='Delete Me', target_value=10)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/goals/{goal.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Goal.objects.filter(id=goal.id).exists())

    def test_cannot_access_other_users_goal(self):
        goal = Goal.objects.create(user=self.other_user, title='Not Mine', target_value=10)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/goals/{goal.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
