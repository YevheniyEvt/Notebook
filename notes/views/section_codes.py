from django.views.generic import ListView, DetailView, CreateView

from notes.models import Code

__all__ = [
    'SectionCodeListView',
]


class SectionCodeListView(ListView):
    model = Code
    context_object_name = 'codes'
    template_name = 'notes/partials/code_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

