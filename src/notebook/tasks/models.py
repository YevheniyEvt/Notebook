from django.contrib.auth.models import User
from django.db import models

__all__ = [
    'Task',
]

from django.urls import reverse


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.title}|{self.end_date}'

    def get_absolute_url(self):
        return reverse('tasks:task_list')