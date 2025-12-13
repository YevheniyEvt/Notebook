from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin
from mixins.view import PkInFormKwargsMixin
from notes.forms import SectionCodeCreateHTMXForm, SectionCodeUpdateHTMXForm
from notes.models import Code, Section

__all__ = [
    'SectionCodeListView',
    'SectionCodeCreateView',
    'SectionCodeUpdateView',
    'SectionCodeDeleteView',
]


class SectionCodeListView(LoginRequiredMixin, ListView):
    model = Code
    context_object_name = 'codes'
    template_name = 'notes/partials/section_code/code_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = Section.objects.get(id=self.kwargs['pk'])
        return context


class SectionCodeCreateView(LoginRequiredMixin, HTMXViewFormMixin, PkInFormKwargsMixin, CreateView):
    model = Code
    form_class = SectionCodeCreateHTMXForm
    template_name = 'notes/partials/section_code/code_form.html'
    htmx_client_events = ['rerenderCodeList']

    def get_queryset(self):
        return super().get_queryset().filter(section__id=self.kwargs['pk'], user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.section_id = self.kwargs['pk']
        messages.success(self.request, 'Code added.')
        return super().form_valid(form)


class SectionCodeUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Code
    form_class = SectionCodeUpdateHTMXForm
    template_name = 'notes/partials/section_code/code_form.html'
    htmx_client_events = ['rerenderCodeList']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Code updated.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['related_instance_id'] = self.object.section_id
        return kwargs

class SectionCodeDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Code

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Code was deleted.')
        return super().delete(request, *args, **kwargs)