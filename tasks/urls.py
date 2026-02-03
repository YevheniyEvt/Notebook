from django.urls import path

from .models import Task
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView, SetTaskStatusView, \
    TaskCommentCreateView, TaskCommentDeleteView

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("detail/<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
    path("update/<int:pk>", TaskUpdateView.as_view(), name="task_update"),
    path("delete/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),

    path("task-completed/<int:pk>", SetTaskStatusView.as_view(new_status=Task.Status.COMPLETED), name="task_complete"),
    path("task-canceled/<int:pk>", SetTaskStatusView.as_view(new_status=Task.Status.CANCELED), name="task_cancel"),
    path("task-open/<int:pk>", SetTaskStatusView.as_view(new_status=Task.Status.IN_PROGRESS), name="task_open"),
    path("task-planned/<int:pk>", SetTaskStatusView.as_view(new_status=Task.Status.IS_PLANNED), name="task_planned"),

    path("comment/create/<int:pk>", TaskCommentCreateView.as_view(), name="comment_create"),
    path("comment/delete/<int:pk>", TaskCommentDeleteView.as_view(), name="comment_delete"),

]
