from django.views.generic import TemplateView, ListView

from tasks.models import Task
from notes.models import Topic


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_with_today_deadline'] = Task.objects.tasks_with_today_deadline().filter(user=self.request.user)
        context['terminated_tasks'] = Task.objects.terminated_tasks().filter(user=self.request.user)
        context['topics'] = Topic.objects.filter(user=self.request.user).order_by('created_at')[:6]
        return context
