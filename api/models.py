from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.created_at)[:19]} - {self.owner} : "{self.content}"'
