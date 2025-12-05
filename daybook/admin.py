from django.contrib import admin

from daybook.models import Entries

# Register your models here.
@admin.register(Entries)
class EntriesAdmin(admin.ModelAdmin):
    list_display = ( 'text', 'title',)