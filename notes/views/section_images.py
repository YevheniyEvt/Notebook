import cloudinary
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from notes.forms import SectionImageForm, SectionImageUpdateForm
from notes.models import Image, Section

__all__ = [
    'SectionImageListView',
    'SectionImageCreateView',
    'SectionImageUpdateView',
    'SectionImageDeleteView',
]

class SectionImageListView(ListView):
    model = Image
    context_object_name = 'images'
    template_name = 'notes/partials/section_image/image_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context


class SectionImageCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Image
    form_class = SectionImageForm
    template_name = 'notes/partials/section_image/image_form.html'
    htmx_client_events = ['rerenderImageList']

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.section_id = self.kwargs['pk']
        messages.success(self.request, 'Image added.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'section_id': self.kwargs['pk']})
        return kwargs

class SectionImageUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Image
    form_class = SectionImageUpdateForm
    template_name = 'notes/partials/section_image/image_update_form.html'
    htmx_client_events = ['rerenderImageList']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Image updated.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'section_id': self.object.section_id})
        return kwargs


class SectionImageDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Image

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        public_id = self.get_object().image_file.public_id
        cloudinary.uploader.destroy(public_id, invalidate=True)
        messages.success(self.request, 'Image was deleted.')
        return super().delete(request, *args, **kwargs)