from django.db import models
from django.conf import settings
from problem_tracker.models import Problem

class Submission(models.Model):
    VERDICT_CHOICES = [
        ("OK", "Accepted"),
        ("WRONG_ANSWER", "Wrong Answer"),
        ("TIME_LIMIT_EXCEEDED", "TLE"),
        ("RUNTIME_ERROR", "Runtime Error"),
        ("COMPILATION_ERROR", "Compilation Error"),
        ("OTHER", "Other"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    verdict = models.CharField(max_length=30, choices=VERDICT_CHOICES)
    language = models.CharField(max_length=50)
    submitted_at = models.DateTimeField()

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.user.username} - {self.problem} - {self.verdict}"