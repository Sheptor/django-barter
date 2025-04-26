from .forms import RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User


class RegistrationView(generic.CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        super().form_valid(form)
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogOutView(LogoutView):
    redirect_authenticated_user = True
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
