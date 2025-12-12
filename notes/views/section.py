from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from notes.forms import SectionForm
from notes.models import Section, Topic

__all__ = [
    'SectionDetail',
    'SectionCreateView',
    'SectionUpdateView',
    'SectionDeleteView',
]


class SectionDetail(DetailView):
    model = Section
    context_object_name = 'section'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SectionCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Section
    form_class = SectionForm
    htmx_client_events = ['rerenderSectionList']
    template_name = 'notes/partials/section_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.topic_id = self.kwargs['pk']
        messages.success(self.request, 'Section created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        return context


class SectionUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Section
    form_class = SectionForm
    htmx_client_events = ['rerenderSectionList']
    template_name = 'notes/partials/section_update_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Section updated.')
        return super().form_valid(form)


class SectionDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Section

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Section was deleted.')
        return super().delete(request, *args, **kwargs)
