from django.conf import settings
from django.db import models


class Attempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mission_slug = models.CharField(max_length=50)
    version = models.PositiveSmallIntegerField(default=1)
    code = models.TextField(max_length=20000)
    quiz_answer = models.CharField(max_length=100)
    score = models.PositiveSmallIntegerField()
    passed = models.BooleanField(default=False)
    details = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'mission_slug'])]


class AuthWindow(models.Model):
    key = models.CharField(max_length=64, unique=True)
    started_at = models.DateTimeField()
    count = models.PositiveIntegerField(default=0)
