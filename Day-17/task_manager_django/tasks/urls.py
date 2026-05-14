from django.urls import path

from .views import HealthCheckView, TaskDetailView, TaskListCreateView

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:task_id>", TaskDetailView.as_view(), name="task-detail"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
