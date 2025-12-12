
from django.views.generic import ListView, DetailView, CreateView

from notes.models import Section

__all__ = [
    'SectionDetail',
]


class SectionDetail(DetailView):
    model = Section
    context_object_name = 'section'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)