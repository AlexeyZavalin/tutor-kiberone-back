from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from authapp.forms import LoginForm


class LoginTutor(LoginView):
    """ Страница входа """
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'authapp/login.html'


def logout_view(request):
    """ Выход из учетной записи """
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse_lazy('authapp:login'))
