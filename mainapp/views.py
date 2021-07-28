from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from mainapp.forms import LoginForm


class MainRedirectView(RedirectView):
    """ Редирект с главной страницы на страницу входа """
    permanent = True
    query_string = False
    url = 'mainapp:login'


class LoginTutor(LoginView):
    """ Страница входа """
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'mainapp/login.html'


def logout_view(request):
    """ Выход из учетной записи """
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse_lazy('mainapp:login'))
