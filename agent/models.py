import markdown
import bleach

from django.contrib.auth.models import User
from django.db import models

from agent.constants import ALLOWED_TAGS, ALLOWED_ATTRS

class Chat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f'Chat #{self.id}'

    class Meta:
        ordering = ['-start_date']


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ai_message = models.BooleanField(default=False)
    is_user_message = models.BooleanField(default=False)

    def __str__(self):
        return self.message[:10]

    def save(self, *args, **kwargs):
        # render markdown → HTML
        html = markdown.markdown(
            self.content,
            extensions=['fenced_code', 'codehilite']
        )
        clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
        self.html_content = clean_html
        super().save(*args, **kwargs)