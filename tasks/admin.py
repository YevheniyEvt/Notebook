from django.contrib import admin

from .models import Task, TaskComment

# Register your models here.
admin.register(Task)
admin.register(TaskComment)