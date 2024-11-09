from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView

from .forms import SignUpForm, CustomUserForm
from .models import CustomUser

# Create your views here.


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy("home")


class CustomLoginView(LoginView):
    template_name = "login.html"


class UserEditView(UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = "user_edit.html"
    success_url = reverse_lazy("user_edit")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """Adding a message for user after saving changes"""
        response = super().form_valid(form)
        # add success message after saving the form
        messages.success(self.request, "Profile updated successfully!")
        return response
