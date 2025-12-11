import random

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.utils.text import slugify

from cloudinary.models import CloudinaryField


DEFAULT_BOOTSTRAP_ICON_NAME = ['calendar2', 'clipboard', 'cpu', 'database', 'file-richtext-fill', 'floppy']

def get_display_name(instance):
    return instance.get_display_name()


def get_public_id_prefix(instance):
    model_name = instance.__class__.__name__
    return f"{model_name}/{instance.get_display_name()}/"

def get_random_icon():
    return random.choice(DEFAULT_BOOTSTRAP_ICON_NAME)

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, 'Must be more then 2 characters')],
    )
    description = models.TextField(max_length=200, blank=True, null=True)
    bootstrap_icon_name=models.CharField(blank=True, null=True, max_length=100, default=get_random_icon)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('notes:topic_detail', kwargs={'pk': self.pk})


class Section(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=200, blank=True, null=True)
    bootstrap_icon_name = models.CharField(blank=True, null=True, max_length=100, default=get_random_icon)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('notes:section_detail', kwargs={'pk': self.pk})


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    image_title = models.CharField(max_length=150)
    image_description = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = CloudinaryField('image',
                                 display_name=get_display_name,
                                 public_id_prefix=get_public_id_prefix,

                                 )

    class Meta:
        ordering = ['-created_at']

    def get_display_name(self):
        return f"Section-{slugify(self.section.title)}-Image-{slugify(self.image_title)}"

    def get_image_url(self):
        if self.image_file is not None:
            return self.image_file.build_url()
        return None

    def get_thumbnail_url(self):
        if self.image_file is not None:
            return self.image_file.build_url(
                width=600,
                height=400,
                crop="pad",
                background="gen_fill:ignore-foreground_true",
                quality="auto"
            )
        return None


class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']