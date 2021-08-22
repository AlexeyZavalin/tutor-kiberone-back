import json

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from mainapp.forms import CreateGroupForm, LoginForm, RemoveGroupForm
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
    """Страница со списком групп для авторизованного тьютора"""
    login_url = reverse_lazy('mainapp:login')
    model = Group
    context_object_name = 'groups'
    template_name = 'mainapp/group/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        days_of_week = Group.active.filter(tutor=self.request.user)\
            .values_list('day_of_week', flat=True).distinct()
        context['groups_by_days'] = []
        for day_of_week in days_of_week:
            groups = Group.active.filter(day_of_week=day_of_week)
            _, day_of_week_display = [day for day in Group.DAYS_OF_WEEK_CHOICES
                                      if day[0] == day_of_week][0]
            context['groups_by_days'].append(
                {
                    'day_of_week': day_of_week_display,
                    'groups': groups
                }
            )

        context['remove_form'] = RemoveGroupForm()
        context['create_group_form'] = CreateGroupForm()
        return context


class RemoveGroup(DeleteView):
    """Прдеставление для удаления группы"""
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        group_id = body.get('group_id')
        password = body.get('password')
        username = request.user.email
        group = get_object_or_404(Group, pk=group_id)
        if group is not None:
            if group.is_deleted:
                return JsonResponse({'success': False,
                                     'message': 'Группа уже удалена'})
            user = authenticate(username=username, password=password)
            if user is not None:
                group.delete()
                return JsonResponse({'success': True})
            return JsonResponse({'success': False,
                                 'message': 'Неверный пароль'})
        return JsonResponse({'success': False,
                             'message': 'Изменилось id '
                                        'группы или где-то'
                                        ' в другом месте ее удалили, '
                                        'обнови странццу'})


class CreateGroupView(CreateView):
    """Представление для создания группы"""
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        location = body.get('location')
        time = body.get('time')
        day_of_week = body.get('day_of_week')
        group = Group.objects.filter(time=time, location=location,
                                     day_of_week=day_of_week)
        if group.exists():
            if group.first().is_deleted:
                group.update(is_deleted=False)
                return JsonResponse({'success': True,
                                     'redirect':
                                         reverse_lazy('mainapp:groups')})
            return JsonResponse({'success': False,
                                 'message': 'Такая группа уже есть, '
                                            'измените параметры'})
        Group.objects.create(location=location, time=time,
                             day_of_week=day_of_week, tutor=request.user)
        return JsonResponse({'success': True,
                             'redirect': reverse_lazy('mainapp:groups')})


class GroupDetailView(LoginRequiredMixin, DetailView):
    """Представление страницы группы"""
    model = Group
    template_name = 'mainapp/group/detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = context['group'].students\
            .filter(is_deleted=False)
        return context
