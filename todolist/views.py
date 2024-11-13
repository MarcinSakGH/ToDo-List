from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    View,
    DeleteView,
)

from .models import Task
from .forms import TaskForm, TaskDetailForm, TaskUpdateForm


# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    login_url = "login"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status_filter = self.request.GET.get("status", "all")
        # If the status parameter is specified, filter tasks based on it
        if status_filter in ["pending", "completed"]:
            queryset = queryset.filter(status=status_filter)

        sort_by = self.request.GET.get("sort", "created_at")
        if sort_by == "created_at":
            queryset = queryset.order_by("created_at")
        elif sort_by == "completed_at":
            queryset = queryset.order_by("completed_at")
        elif sort_by == "due_date":
            queryset = queryset.order_by("due_date")

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
        return self.get(request, *args, **kwargs)


class AddTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskDetailForm
    template_name = "add_task.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditTaskView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "task_update.html"

    def get_success_url(self):
        success_url = reverse_lazy("task_update", kwargs={"pk": self.object.pk})
        return success_url

    def form_valid(self, form):
        """Adding a message for user after saving changes"""
        response = super().form_valid(form)
        # add success message after saving the form
        messages.success(self.request, "Task was updated succesfully!")
        return response


class MarkTaskAsCompletedView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.completed_at:
            task.completed_at = None
            task.status = task.PENDING
        else:
            task.mark_as_completed()

        task.save()

        # Retrieve the current filter from the request and redirect back to TaskListView with the filter applied
        filter_status = request.POST.get("status", "all")
        sort_by = request.GET.get("sort", "created_at")
        return redirect(f"/task-list/?sort={sort_by}&status={filter_status}")


class DeleteTaskView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task_list")
