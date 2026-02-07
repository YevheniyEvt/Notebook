import random
import uuid

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:sections_list', kwargs={'pk': self.pk})

    def get_update_url(self, **kwargs):
        return reverse('notes:topic_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:topic_create')

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:topic_list')


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

    def get_update_url(self, **kwargs):
        return reverse('notes:section_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:section_create', kwargs={'pk': kwargs['related_instance_id']})

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:sections_list', kwargs={'pk': kwargs['related_instance_id']})


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_update_url(self, **kwargs):
        return reverse('notes:code_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:code_create', kwargs={'pk': kwargs['related_instance_id']})

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:code_list', kwargs={'pk': kwargs['related_instance_id']})

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_update_url(self, **kwargs):
        return reverse('notes:article_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:article_create', kwargs={'pk': kwargs['related_instance_id']})

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:article_list', kwargs={'pk': kwargs['related_instance_id']})


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = CloudinaryField('image',
                                 display_name=get_display_name,
                                 public_id_prefix=get_public_id_prefix,
                                 )

    class Meta:
        ordering = ['-created_at']

    def get_display_name(self):
        return f"Section-{slugify(self.section.title)}-Image-{slugify(self.title) if self.title else uuid.uuid4()}"

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

    def get_update_url(self, **kwargs):
        return reverse('notes:image_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:image_create', kwargs={'pk': kwargs['related_instance_id']})

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:image_list', kwargs={'pk': kwargs['related_instance_id']})


class Links(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.URLField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_update_url(self, **kwargs):
        return reverse('notes:link_update', kwargs={'pk': self.id})

    @classmethod
    def get_create_url(cls, **kwargs):
        return reverse('notes:link_create', kwargs={'pk': kwargs['related_instance_id']})

    @classmethod
    def get_hx_rerender_url(cls, **kwargs):
        return reverse('notes:link_list', kwargs={'pk': kwargs['related_instance_id']})
