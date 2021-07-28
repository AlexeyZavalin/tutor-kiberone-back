from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView

from mainapp.forms import LoginForm
from mainapp.models import Group


class MainRedirectView(RedirectView):
    """ Редирект с главной страницы на страницу входа """
    permanent = True
    query_string = False
    pattern_name = 'mainapp:login'


class LoginTutor(LoginView):
    """ Страница входа """
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'mainapp/login.html'


def logout_view(request):
    """ Выход из учетной записи """
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse_lazy('mainapp:login'))


class GroupListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('mainapp:login')
    model = Group
    context_object_name = 'groups'
    template_name = 'mainapp/group/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        days_of_week = Group.objects.filter(tutor=self.request.user)\
            .values_list('day_of_week', flat=True).distinct()
        context['groups_by_days'] = []
        for day_of_week in days_of_week:
            groups = Group.objects.filter(day_of_week=day_of_week)
            _, day_of_week_display = [day for day in Group.DAYS_OF_WEEK_CHOICES if day[0] == day_of_week][0]
            context['groups_by_days'].append(
                {
                    'day_of_week': day_of_week_display,
                    'groups': groups
                }
            )
        return context
