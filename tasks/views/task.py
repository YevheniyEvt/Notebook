from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event
from django_tables2 import SingleTableView

from mixins import HTMXViewFormMixin
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task

from tasks.table import TaskTable

__all__ = [
    'TaskListView',
    'TaskDetailView',
    'TaskCreateView',
    'TaskUpdateView',
    'TaskDeleteView',
    'SetTaskStatusView',
]

class TaskListView(FilterView, SingleTableView):
    model = Task
    table_class = TaskTable
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name + '#django_table'
        return self.template_name


class TaskDetailView(DeleteView):
    model = Task
    template_name = 'tasks/partials/detail_task_modal.html'
    context_object_name = 'task'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TaskCreateView(HTMXViewFormMixin, CreateView):
    model = Task
    template_name = 'tasks/partials/create_task_modal.html'
    form_class = TaskForm
    htmx_client_events = ['rerenderTaskTable', 'closeModal']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(HTMXViewFormMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/partials/create_task_modal.html'
    htmx_client_events = ['rerenderTaskTable', 'closeModal']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TaskDeleteView(DeleteView):
    model = Task
    http_method_names = ['delete']
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        response = HttpResponse()
        trigger_client_event(response, 'rerenderTaskTable')
        return response


class SetTaskStatusView(UpdateView):
    model = Task
    http_method_names = ['post']
    new_status = None

    def dispatch(self, request, *args, **kwargs):
        if self.new_status is None or self.new_status not in Task.Status:
            raise AttributeError(
                f'new_status attr must be specified. Choices are {Task.Status.values}'
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        self.set_task_status(task)
        response = HttpResponse()
        trigger_client_event(response, 'rerenderTaskTable')
        trigger_client_event(response, 'closeModal')
        return response

    def set_task_status(self, task):
        task.status = self.new_status
        task.save()
