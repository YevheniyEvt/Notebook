from django.contrib.auth.models import User
from django.db import models

class Entries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField()


    def __str__(self):
        return f'{self.created_at} "{self.title or self.text[0:50]}..."'

    class Meta:
        ordering = ['-created_at']