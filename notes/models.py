from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

from cloudinary.models import CloudinaryField


# Create your models here.

def get_display_name(instance):
    return instance.get_display_name()


def get_public_id_prefix(instance):
    model_name = instance.__class__.__name__
    return f"{model_name}/{instance.get_display_name()}/"


class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, 'Must be more then 2 characters')],
    )
    short_description = models.TextField(blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-add_date']


class Section(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True, default=None)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-add_date']


class Code(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    image_title = models.CharField(max_length=150)
    image_description = models.TextField(blank=True, null=True, default=None)
    add_date = models.DateTimeField(auto_now_add=True)
    image_file = CloudinaryField('image',
                                 display_name=get_display_name,
                                 public_id_prefix=get_public_id_prefix,

                                 )

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
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    url = models.URLField()
    add_date = models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.date} "{self.text[0:50]}..."'

    class Meta:
        ordering = ['-date']