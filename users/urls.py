from django.urls import path, include

from . import views

app_name = "users"
urlpatterns = [
    path("registration/", views.registration_view, name="registration"),
    path("login/", views.LogInView.as_view(), name="login")
]
