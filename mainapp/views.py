import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from .forms import CreateGroupForm, RemoveGroupForm, CreateStudentForm
from .models import Group
from .services import get_response_for_create_group, \
    get_response_for_remove_group, get_response_for_create_student


class MainRedirectView(RedirectView):
    """ Редирект с главной страницы на страницу входа """
    permanent = True
    query_string = False
    pattern_name = 'authapp:login'


class GroupListView(LoginRequiredMixin, ListView):
    """Страница со списком групп для авторизованного тьютора"""
    login_url = reverse_lazy('authapp:login')
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
        return get_response_for_remove_group(group_id=body.get('group_id'),
                                             password=body.get('password'),
                                             username=request.user.email)


class CreateGroupView(CreateView):
    """Представление для создания группы"""
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_create_group(location=body.get('location'),
                                             time=body.get('time'),
                                             day_of_week=body.get(
                                                 'day_of_week'),
                                             user=request.user)


class GroupDetailView(LoginRequiredMixin, DetailView):
    """Представление страницы группы"""
    model = Group
    template_name = 'mainapp/group/detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = context['group'].students\
            .filter(is_deleted=False)
        context['create_student_form'] = CreateStudentForm()
        return context


class CreateStudentView(CreateView):
    """Представление для добавления студента в группу"""
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_create_student(name=body.get('name'),
                                               kiberon_amount=body.get(
                                                   'kiberon_amount'),
                                               info=body.get('info'),
                                               group_id=kwargs.get('group_id'))
