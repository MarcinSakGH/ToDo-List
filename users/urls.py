from django.urls import include, path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, CustomLoginView, UserEditView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('edit-profile/', UserEditView.as_view(), name='user_edit')
]
