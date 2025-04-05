from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy


def home_view(request):
    return HttpResponse("Home page")


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    form = RegistrationForm()
    return render(request, "users/registration.html", {"form": form})


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))
