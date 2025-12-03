from datetime import date

from django.contrib.auth.models import User
from django.db import models

__all__ = [
    'Task',
]

from django.urls import reverse

class Task(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'completed'
        IN_PROGRESS = 'in_progress'
        CANCELED = 'canceled'

    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    status = models.CharField(choices=Status.choices, default=Status.IN_PROGRESS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('end_date',)

    def __str__(self):
        return f'{self.title}|{self.end_date}'

    def get_absolute_url(self):
        return reverse('tasks:task_list')

    @property
    def is_completed(self):
        return self.status == Task.Status.COMPLETED

    @property
    def is_in_progress(self):
        return self.status == Task.Status.IN_PROGRESS

    @property
    def is_canceled(self):
        return self.status == Task.Status.CANCELED

    @property
    def is_terminated(self):
        return self.end_date < date.today()

    @property
    def can_be_completed(self):
        return self.is_in_progress

    @property
    def can_be_canceled(self):
        return self.is_in_progress

    @property
    def can_be_opened(self):
        return self.is_canceled or self.is_completed

