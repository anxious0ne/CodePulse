from django.conf import settings
from django.db import models


GOAL_TYPE_CHOICES = [
    ('problems_solved', 'Problems Solved'),
    ('rating', 'Rating Target'),
    ('contests', 'Contests Participated'),
    ('custom', 'Custom Goal'),
]


class Goal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPE_CHOICES, default='custom')
    target_value = models.IntegerField(default=0)
    current_value = models.IntegerField(default=0)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.title}'

    @property
    def progress_percentage(self):
        if self.target_value > 0:
            return min(100, int((self.current_value / self.target_value) * 100))
        return 0
