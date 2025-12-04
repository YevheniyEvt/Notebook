from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django_htmx.http import trigger_client_event

__all__ = [
    'HTMXViewFormMixin',
]

class HTMXViewFormMixin:
    """
    A mixin for Django class-based views that are intended to be accessed exclusively
    via HTMX requests.

    Features:
        - Redirects all non-HTMX requests to `redirect_url`.
        - Provides a list of HTMX client-side events to trigger after a successful
          form submission.
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
    htmx_client_events: list[str] = []

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

