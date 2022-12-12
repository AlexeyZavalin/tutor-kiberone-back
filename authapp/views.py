from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from authapp.forms import LoginForm, TutorPasswordChangeForm, StudentLoginForm

from mainapp.models import Student


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


def logout_student(request):
    """ Выход из учетной записи ученика"""
    try:
        del request.session['student']
    except KeyError:
        pass
    response = HttpResponseRedirect(redirect_to=reverse_lazy('authapp:login'))
    response.delete_cookie('student_token')
    return response


class LoginStudent(FormView):
    form_class = StudentLoginForm
    template_name = 'authapp/login_student.html'
    success_url = reverse_lazy('mainapp:student_personal_area')
    
    def form_valid(self, form):
        student = Student.objects.get(
            code=form.cleaned_data.get('password')
        )
        self.request.session['student'] = student.token
        response = super(LoginStudent, self).form_valid(form)
        response.set_cookie('student_token', student.token)
        return response
