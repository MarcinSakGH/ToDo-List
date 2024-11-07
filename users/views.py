from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import SignUpForm
from .models import CustomUser

# Create your views here.


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy('home')


class CustomLoginView(LoginView):
    template_name = "login.html"
