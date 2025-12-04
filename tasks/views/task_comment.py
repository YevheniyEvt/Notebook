from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django_htmx.http import trigger_client_event

from tasks.forms import TaskCommentForm
from tasks.models import Task, TaskComment

__all__ = [
    'TaskCommentCreateView',
    'TaskCommentDeleteView',
]

class TaskCommentCreateView(CreateView):
    model = TaskComment
    form_class = TaskCommentForm
    template_name = 'tasks/partials/create_task_comment_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.task = task
        if self.request.htmx:
            form.save()
            response = self.render_to_response({'form': form, 'task': task})
            trigger_client_event(response, 'refreshTaskDetail')
            return response

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        return context

class TaskCommentDeleteView(DeleteView):
    model = TaskComment

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        if self.request.htmx:
            self.get_object().delete()
            response = HttpResponse()
            trigger_client_event(response, 'refreshTaskDetail')
            return response

        return super().delete(request, *args, **kwargs)
