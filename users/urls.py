from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

app_name = "users"
urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]
