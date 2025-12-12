from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from notes.forms import SectionLinksForm
from notes.models import Links, Section

__all__ = [
    'SectionLinksListView',
    'SectionLinksCreateView',
    'SectionLinksUpdateView',
    'SectionLinksDeleteView',
]


class SectionLinksListView(ListView):
    model = Links
    context_object_name = 'links'
    template_name = 'notes/partials/section_links/links_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context


class SectionLinksCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Links
    form_class = SectionLinksForm
    template_name = 'notes/partials/section_links/links_form.html'
    htmx_client_events = ['rerenderLinksList']

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.section_id = self.kwargs['pk']
        messages.success(self.request, 'Links added.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context


class SectionLinksUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Links
    form_class = SectionLinksForm
    template_name = 'notes/partials/section_links/links_update_form.html'
    htmx_client_events = ['rerenderLinksList']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Links updated.')
        return super().form_valid(form)


class SectionLinksDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Links

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Links was deleted.')
        return super().delete(request, *args, **kwargs)