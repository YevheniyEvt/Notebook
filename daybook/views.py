from django.views.generic import ListView, CreateView, UpdateView

from daybook.forms import EntriesForm
from daybook.models import Entries
from mixins import HTMXViewFormMixin


class EntriesList(ListView):
    model = Entries
    template_name = 'daybook/entries_list.html'


class EntriesCreateView(HTMXViewFormMixin, CreateView):
    model = Entries
    form_class = EntriesForm
    template_name = 'daybook/partials/create_entries_modal.html'
    htmx_client_events = ['rerenderEntriesList', 'closeModal']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntriesUpdateView(HTMXViewFormMixin, UpdateView):
    model = Entries
    form_class = EntriesForm
    template_name = 'daybook/partials/create_entries_modal.html'
    htmx_client_events = ['rerenderEntriesList', 'closeModal']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)