from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event

from agent.filter import ChatFilter
from agent.forms import MessageCreateForm
from agent.models import Message, Chat
from agent.utils import llm_response_generator
from mixins.view import PkInFormKwargsMixin, HTMXViewFormMixin, HTMXDeleteViewMixin


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.chat = Chat.objects.create(user=request.user)
        response = HttpResponse()
        trigger_client_event(response, 'rerenderChat')
        return response


class ChatDeleteView(LoginRequiredMixin, HTMXDeleteViewMixin, DeleteView):
    model = Chat
    htmx_client_events = ["rerenderChat",]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'agent/partials/chat_detail.html'
    context_object_name = 'chat'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ChatListView(LoginRequiredMixin, FilterView, ListView):
    model = Chat
    filterset_class = ChatFilter
    template_name = 'agent/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name + '#chatbot'
        return self.template_name

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        ctx = super().get_context_data()
        ctx['search'] = search
        return ctx


class MessageCreateView(LoginRequiredMixin, PkInFormKwargsMixin, HTMXViewFormMixin, CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'agent/partials/message_form.html'
    htmx_client_events = ['rerenderMessages',]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        chat = Chat.objects.get(pk=self.kwargs['pk'])
        if not chat.name:
            chat.name = f"{form.cleaned_data['content'][:30]}"
            chat.save()
            self.htmx_client_events = ['rerenderChat',]
        form.instance.chat_id = self.kwargs['pk']
        form.instance.user = self.request.user
        form.instance.is_user_message = True
        form.save()

        llm_response = llm_response_generator(chat)
        llm_answer = llm_response['messages'][-1].content
        Message.objects.create(
            chat=chat,
            user=self.request.user,
            is_ai_message=True,
            content=llm_answer,
        )
        return super().form_valid(form)