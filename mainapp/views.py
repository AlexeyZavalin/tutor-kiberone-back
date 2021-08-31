import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from .forms import BulkStudentActionsForm, CreateGroupForm, CreateStudentForm,\
    RemoveGroupForm, RemoveStudentForm
from .models import Group, Student
from .services import form_data_processing, get_response_for_create_group, \
    get_response_for_create_student, get_response_for_remove_group, \
    get_response_for_remove_student


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
        days_of_week = Group.active.filter(tutor=self.request.user) \
            .values_list('day_of_week', flat=True).distinct()
        context['groups_by_days'] = []
        for day_of_week in days_of_week:
            groups = Group.active.filter(day_of_week=day_of_week,
                                         tutor=self.request.user)
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


class StudentListView(LoginRequiredMixin, ListView):
    """Список студентов группы"""
    model = Student
    template_name = 'mainapp/student/list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.active.filter(group_id=self.kwargs.get('group_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(pk=self.kwargs.get('group_id'))
        context['create_student_form'] = CreateStudentForm()
        context['remove_student_form'] = RemoveStudentForm()
        context['bulk_action_form'] = BulkStudentActionsForm()
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


class RemoveStudent(DeleteView):
    """Прдеставление для удаления студента"""

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_remove_student(student_id=body
                                               .get('student_id'),
                                               password=body.get('password'),
                                               username=request.user.email)


@require_http_methods(['POST'])
def bulk_update_students(request, group_id):
    """Представление для массовой обработки студентов"""
    form = BulkStudentActionsForm(request.POST)
    if form.is_valid():
        form_data_processing(data=form.cleaned_data, tutor=request.user)
    return HttpResponseRedirect(reverse_lazy('mainapp:student-list',
                                             kwargs={'group_id': group_id}))
