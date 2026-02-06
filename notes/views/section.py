import cloudinary
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from mixins.view import PkInFormKwargsMixin
from notes.filter import SectionFilter
from notes.forms import SectionCreateHTMXForm, SectionUpdateHTMXForm
from notes.models import Section, Topic

__all__ = [
    'SectionDetail',
    'SectionCreateView',
    'SectionUpdateView',
    'SectionDeleteView',
    'SectionListView',
]

class SectionListView(LoginRequiredMixin, FilterView, ListView):
    model = Section
    filterset_class = SectionFilter
    context_object_name = 'sections'
    template_name = 'notes/topic_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, topic_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        context['topic'] = topic
        return context

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name + '#sections'
        return self.template_name

class SectionDetail(DetailView):
    model = Section
    context_object_name = 'section'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SectionCreateView(LoginRequiredMixin, HTMXViewFormMixin, PkInFormKwargsMixin, CreateView):
    model = Section
    form_class = SectionCreateHTMXForm
    htmx_client_events = ['rerenderSectionList']
    template_name = 'notes/partials/section_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.topic_id = self.kwargs['pk']
        messages.success(self.request, 'Section created.')
        return super().form_valid(form)


class SectionUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Section
    form_class = SectionUpdateHTMXForm
    htmx_client_events = ['rerenderSectionList']
    template_name = 'notes/partials/section_update_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Section updated.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['related_instance_id'] = self.object.topic_id
        return kwargs

class SectionDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Section

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        images = self.get_object().image_set.all()
        for image in images:
            public_id = image.image_file.public_id
            cloudinary.uploader.destroy(public_id, invalidate=True)
        messages.success(self.request, 'Section was deleted.')
        return super().delete(request, *args, **kwargs)
