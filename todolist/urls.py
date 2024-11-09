from django.urls import path
from .views import (
    HomePageView,
    TaskListView,
    AddTaskView,
    EditTaskView,
    MarkTaskAsCompletedView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("task-list/", TaskListView.as_view(), name="task_list"),
    path("add-task/", AddTaskView.as_view(), name="add_task"),
    path("update-task/<int:pk>/", EditTaskView.as_view(), name="task_update"),
    path(
        "task/completed/<int:pk>/",
        MarkTaskAsCompletedView.as_view(),
        name="task_completed",
    ),
]
