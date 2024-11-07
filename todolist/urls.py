from django.urls import path
from .views import HomePageView, TaskListView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('task-list/', TaskListView.as_view(), name="task_list"),
]
