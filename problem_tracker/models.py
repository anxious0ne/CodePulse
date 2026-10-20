from django.db import models


class Problem(models.Model):
    contest_id = models.IntegerField()
    problem_index = models.CharField(max_length=10)   # e.g. "A", "B2"
    name = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, blank=True)
    tags = models.JSONField(default=list)   # e.g. ["dp", "graphs"]

    class Meta:
        unique_together = ("contest_id", "problem_index")

    def __str__(self):
        return f"{self.contest_id}{self.problem_index} - {self.name}" 