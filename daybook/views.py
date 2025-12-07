from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_htmx.http import HttpResponseClientRefresh

from daybook.forms import EntriesUpdateForm, EntriesCreateForm
from daybook.models import Entries
from mixins import HTMXViewFormMixin


class EntriesListView(ListView):
    model = Entries
    template_name = 'daybook/entries_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EntriesDetailView(DetailView):
    model = Entries
    template_name = 'daybook/entries_list.html#entry'
    context_object_name = 'entry'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EntriesCreateView(CreateView):
    model = Entries
    form_class = EntriesCreateForm
    template_name = 'daybook/partials/create_entries_modal.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return HttpResponseClientRefresh()


class EntriesUpdateView(HTMXViewFormMixin, UpdateView):
    model = Entries
    form_class = EntriesUpdateForm
    template_name = 'daybook/partials/update_enty_form.html'
    htmx_client_events = []

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        entry = self.get_object()
        self.htmx_client_events.append(f'rerenderEntry{entry.id}')
        return super().post(request, *args, **kwargs)


class EntriesDeleteView(DeleteView):
    model = Entries

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        response = HttpResponse()
        return response