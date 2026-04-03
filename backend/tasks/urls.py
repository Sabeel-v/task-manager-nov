from django.urls import path
from .views import get_tasks, update_task, task_report

urlpatterns = [
    path('tasks/', get_tasks),
    path('tasks/<int:id>/', update_task),
    path('tasks/<int:id>/report/', task_report),
]