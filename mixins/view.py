from typing import Sequence

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django_htmx.http import trigger_client_event

__all__ = [
    'HTMXViewFormMixin',
    'HTMXDeleteViewMixin',
]

class HTMXViewFormMixin:
    """
    A mixin for Django class-based views that are intended to be accessed exclusively
    via HTMX requests.

    Features:
        - Redirects all non-HTMX requests to `redirect_url`.
        - Provides a list of HTMX client-side events to trigger after a successful
          form submission.
        - Provides a send message events for creating toast.
        - Simplifies creation of HTMX-only form views.

    Attributes:
        redirect_url (str):
            The URL to redirect to when a non-HTMX request is received.
            Defaults to `reverse_lazy('notebook:index')`.

        htmx_client_events (list[str]):
            A list of event names that will be emitted to the HTMX client after
            `form_valid()` is executed.

    Typical use:
        - Use this mixin together with Django's FormView/CreateView/UpdateView.
    """

    redirect_url: str = reverse_lazy('index')
    htmx_client_events: Sequence[str] = []

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response = HttpResponse()
        for client_event in self.htmx_client_events:
            trigger_client_event(response, client_event)
        return response


class HTMXDeleteViewMixin:
    """
    A mixin for Django class-based views that are intended to be accessed exclusively
    via HTMX requests.

    Features:
        - Provides a list of HTMX client-side events to trigger after deletion

    Attributes:
        htmx_client_events (list[str]):
            A list of event names that will be emitted to the HTMX client after
            `form_valid()` is executed.

    Typical use:
        - Use this mixin together with Django's DeleteView.
    """
    http_method_names = ['delete']
    htmx_client_events: Sequence[str] = []

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        response = HttpResponse()
        for client_event in self.htmx_client_events:
            trigger_client_event(response, client_event)
        return response

class PkInFormKwargsMixin:
    """
    Add pk from kwargs to form kwargs.
    In for it should be pop.
    Example:
        def __init__(self, *args, **kwargs):
        self.related_instance_id = kwargs.pop('related_instance_id')
        super().__init__(*args, **kwargs)
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['related_instance_id'] = self.kwargs['pk']
        return kwargs