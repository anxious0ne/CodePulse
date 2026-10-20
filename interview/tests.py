from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import InterviewQuestion, UserQuestionProgress

User = get_user_model()


class InterviewQuestionTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='ivuser', password='Pass123!')
        self.q1 = InterviewQuestion.objects.create(
            title='Two Sum', category='arrays', difficulty='easy'
        )
        self.q2 = InterviewQuestion.objects.create(
            title='Longest Substring', category='strings', difficulty='medium'
        )
        self.q3 = InterviewQuestion.objects.create(
            title='Coin Change', category='dp', difficulty='medium'
        )

    def test_unauthenticated_cannot_list_questions(self):
        response = self.client.get('/api/interview/questions/')
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_can_list_all_questions(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/interview/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', response.data)
        self.assertGreaterEqual(len(data), 3)

    def test_filter_by_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/interview/questions/?category=arrays')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', response.data)
        for item in data:
            self.assertEqual(item['category'], 'arrays')

    def test_filter_by_difficulty(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/interview/questions/?difficulty=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data if isinstance(response.data, list) else response.data.get('results', response.data)
        for item in data:
            self.assertEqual(item['difficulty'], 'medium')

    def test_mark_question_completed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f'/api/interview/progress/{self.q1.id}/',
            {'is_completed': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_completed'])

    def test_bookmark_question(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f'/api/interview/progress/{self.q1.id}/',
            {'is_bookmarked': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_bookmarked'])

    def test_get_progress_for_question(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/interview/progress/{self.q2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_completed'])
