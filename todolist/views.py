from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View

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
        return Task.objects.filter(user=self.request.user)

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
        elif not task.completed_at:
            task.mark_as_completed()

        task.save()
        return redirect("task_list")
