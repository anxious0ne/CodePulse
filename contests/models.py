from django.db import models
from django.conf import settings


class Contest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contests"
    )
    contest_id = models.IntegerField()
    contest_name = models.CharField(max_length=255)
    rank = models.IntegerField()
    old_rating = models.IntegerField()
    new_rating = models.IntegerField()
    rating_update_time = models.DateTimeField()

    class Meta:
        unique_together = ("user", "contest_id")
        ordering = ["rating_update_time"]

    def __str__(self):
        return f"{self.user.username} - {self.contest_name}"