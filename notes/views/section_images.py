from django.views.generic import ListView, DetailView, CreateView

from notes.models import Image

__all__ = [
    'SectionImageListView',
]


class SectionImageListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'notes/partials/images_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)