from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView

from daybook.filter import EntriesFilter
from daybook.forms import EntriesUpdateForm, EntriesCreateForm
from daybook.models import Entries
from mixins import HTMXViewFormMixin, HTMXDeleteViewMixin


class EntriesListView(LoginRequiredMixin, FilterView, ListView):
    model = Entries
    template_name = 'daybook/entries_list.html'
    filterset_class = EntriesFilter
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name + '#entries-list'
        return self.template_name


class EntriesDetailView(LoginRequiredMixin, DetailView):
    model = Entries
    template_name = 'daybook/entries_list.html#entry'
    context_object_name = 'entry'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EntriesCreateView(LoginRequiredMixin, HTMXViewFormMixin, CreateView):
    model = Entries
    form_class = EntriesCreateForm
    template_name = 'daybook/partials/create_entries_modal.html'
    htmx_client_events = ['renderEntriesList', 'closeModal']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Entries was created.')
        return super().form_valid(form)


class EntriesUpdateView(LoginRequiredMixin, HTMXViewFormMixin, UpdateView):
    model = Entries
    form_class = EntriesUpdateForm
    template_name = 'daybook/partials/update_enty_form.html'
    htmx_client_events = []

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        entry = self.get_object()
        self.htmx_client_events.append(f'rerenderEntry{entry.id}')
        messages.success(self.request, 'Entries was updated.')
        return super().post(request, *args, **kwargs)


class EntriesDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Entries

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Entries was deleted.')
        return super().delete(request, *args, **kwargs)