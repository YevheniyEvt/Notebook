from django.views.generic import ListView, DetailView, CreateView

from notes.models import Article

__all__ = [
    'SectionArticleListView',
]


class SectionArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'notes/partials/article_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)
