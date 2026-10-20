from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    codeforces_handle = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    is_handle_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username