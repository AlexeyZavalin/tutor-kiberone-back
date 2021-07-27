from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy

from mainapp.models import Tutor
from mainapp.forms import LoginForm


class LoginTutor(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'mainapp/login.html'
    # redirect_field_name = reverse('groups')


def LogoutTutor(LogoutView):
    """ Выход из учетной записи """
    pass


class MainRedirectView(RedirectView):
    permanent = True
    query_string = False
    url = '/login/'
