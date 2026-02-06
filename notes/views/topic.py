from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from notes.filter import SectionTopicFilter
from notes.forms import TopicCreateHTMXForm, TopicUpdateHTMXForm
from notes.models import Topic

__all__ = [
    'TopicListView',
    'TopicCreateView',
    'TopicUpdateView',
    'TopicDeleteView',
]


class TopicListView(LoginRequiredMixin, FilterView, ListView):
    model = Topic
    filterset_class = SectionTopicFilter
    context_object_name = 'topics'
    template_name = 'notes/topic_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name + '#topic-list'
        return self.template_name


class TopicCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Topic
    form_class = TopicCreateHTMXForm
    htmx_client_events = ['rerenderTopicList']
    template_name = 'notes/partials/topic_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Topic created.')
        return super().form_valid(form)


class TopicUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Topic
    form_class = TopicUpdateHTMXForm
    htmx_client_events = ['rerenderTopicList']
    template_name = 'notes/partials/topic_update_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Topic updated.')
        return super().form_valid(form)


class TopicDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Topic

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Topic was deleted.')
        return super().delete(request, *args, **kwargs)

