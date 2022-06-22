from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.


def logout_request(request):
    logout(request)
    messages.info(request, "You logged out successfully!")


    return redirect("login")


class RegisterView(CreateView):
    form_class =UserCreationForm
    model = User
    template_name='authi/register.html'

    def get_success_url(self) -> str:
        return reverse('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register'] = True
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'error')
        print('eror')
        return super().form_invalid(form)

    def form_valid(self, form) :
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class MyLoginView(LoginView):
    template_name = 'authi/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register'] = False
        return context

    def get_success_url(self) -> str:
        return reverse('lobby')
