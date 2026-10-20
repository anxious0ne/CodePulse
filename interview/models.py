from django.conf import settings
from django.db import models


CATEGORY_CHOICES = [
    ('arrays', 'Arrays'),
    ('strings', 'Strings'),
    ('dp', 'Dynamic Programming'),
    ('graphs', 'Graphs'),
    ('trees', 'Trees'),
    ('sorting', 'Sorting'),
    ('binary_search', 'Binary Search'),
    ('greedy', 'Greedy'),
    ('math', 'Math'),
    ('other', 'Other'),
]

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]


class InterviewQuestion(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    link = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'difficulty', 'title']

    def __str__(self):
        return self.title


class UserQuestionProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='question_progress'
    )
    question = models.ForeignKey(
        InterviewQuestion,
        on_delete=models.CASCADE,
        related_name='user_progress'
    )
    is_completed = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('user', 'question')]

    def __str__(self):
        return f'{self.user.username} - {self.question.title}'
