from django.contrib.messages import get_messages
from django_htmx.http import trigger_client_event

class HTMXMessagesMiddleware:
    """
    Intercepts Django messages and converts them to HTMX sendMessages events
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.htmx:
            storage = get_messages(request)
            for message in storage:
                trigger_client_event(
                    response,
                    "sendMessages",
                    {
                        "message": message.message,
                        "tags": message.tags
                    }
                )
            storage.used = True

        return response