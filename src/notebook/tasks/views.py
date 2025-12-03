from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_htmx.http import HttpResponseClientRedirect

from .forms import TaskForm
from .models import Task
from django_tables2 import SingleTableView

from .table import TaskTable


class TaskListView(SingleTableView):
    model = Task
    table_class = TaskTable
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(DeleteView):
    model = Task
    template_name = 'tasks/partials/detail_task_modal.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/partials/create_task_modal.html'
    form_class = TaskForm

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.htmx:
            return HttpResponseClientRedirect(reverse('tasks:task_list'))
        return response


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/partials/create_task_modal.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        if self.request.htmx:
            return HttpResponseClientRedirect(reverse('tasks:task_list'))
        return response


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return HttpResponse()


class SetTaskStatusView(UpdateView):
    model = Task
    action = None

    def dispatch(self, request, *args, **kwargs):
        if self.action is None:
            raise AttributeError('Action must be specified')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        self.set_task_status(task)
        return HttpResponseClientRedirect(reverse('tasks:task_list'))

    def set_task_status(self, task):
        if self.action == task.Status.COMPLETED:
            task.status = task.Status.COMPLETED
            task.save()
        elif self.action == task.Status.IN_PROGRESS:
            task.status = task.Status.IN_PROGRESS
            task.save()
        elif self.action == task.Status.CANCELED:
            task.status = task.Status.CANCELED
            task.save()