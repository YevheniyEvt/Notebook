from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from notes.forms import SectionArticleCreateForm, SectionArticleUpdateForm
from notes.models import Article, Section

__all__ = [
    'SectionArticleListView',
    'SectionArticleCreateView',
    'SectionArticleUpdateView',
    'SectionArticleDeleteView',
]


class SectionArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'notes/partials/section_article/article_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context
    

class SectionArticleCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Article
    form_class = SectionArticleCreateForm
    template_name = 'notes/partials/section_article/article_form.html'
    htmx_client_events = ['rerenderArticleList']

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.section_id = self.kwargs['pk']
        messages.success(self.request, 'Article added.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['section_id'] = self.kwargs['pk']
        return kwargs


class SectionArticleUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Article
    form_class = SectionArticleUpdateForm
    template_name = 'notes/partials/section_article/article_update_form.html'
    htmx_client_events = ['rerenderArticleList']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Article updated.')
        return super().form_valid(form)


class SectionArticleDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Article

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Article was deleted.')
        return super().delete(request, *args, **kwargs)