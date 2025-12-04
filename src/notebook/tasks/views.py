from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_htmx.http import HttpResponseClientRedirect
from django_tables2 import SingleTableView

from .filter import TaskFilter
from .forms import TaskForm, TaskCommentForm
from .models import Task, TaskComment

from .table import TaskTable


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


class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/partials/create_task_modal.html'
    form_class = TaskForm

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.htmx:
            form.save()
            return HttpResponseClientRedirect(reverse('tasks:task_list'))
        response = super().form_valid(form)
        return response


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/partials/create_task_modal.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.htmx:
            form.save()
            return HttpResponseClientRedirect(reverse('tasks:task_list'))
        response = super().form_valid(form)
        return response


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return HttpResponse()


class SetTaskStatusView(UpdateView):
    model = Task
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
        return HttpResponseClientRedirect(reverse('tasks:task_list'))

    def set_task_status(self, task):
        task.status = self.new_status
        task.save()


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
            return self.render_to_response({'form': form, 'task': task})
        response = super().form_valid(form)
        return response

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
            return HttpResponse()
        return super().delete(request, *args, **kwargs)
