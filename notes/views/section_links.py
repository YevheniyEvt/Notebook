from django.views.generic import ListView, DetailView, CreateView

from notes.models import Links

__all__ = [
    'SectionLinksListView',
]


class SectionLinksListView(ListView):
    model = Links
    context_object_name = 'links'
    template_name = 'notes/partials/links_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)
