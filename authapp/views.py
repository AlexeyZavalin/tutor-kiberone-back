from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from authapp.forms import LoginForm, TutorPasswordChangeForm


class LoginTutor(auth_views.LoginView):
    """ Страница входа """
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'authapp/login.html'


def logout_view(request):
    """ Выход из учетной записи """
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse_lazy('authapp:login'))


class TutorPasswordChangeView(auth_views.PasswordChangeView):
    form_class = TutorPasswordChangeForm
    success_url = reverse_lazy('authapp:password-change')
    template_name = 'authapp/password_change.html'
    title = _('Password change')
