from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from .models import Task
from .forms import TaskForm

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    login_url = 'login'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = TaskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        return self.get(request, *args, **kwargs)

