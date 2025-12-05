from django.contrib.auth.models import User
from django.db import models

class Entries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.date} "{self.text[0:50]}..."'

    class Meta:
        ordering = ['-date']