import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import BulkStudentActionsForm, CreateGroupForm, CreateStudentForm, \
    RemoveGroupForm, RemoveStudentForm, UpdateStudentForm
from .models import Group, Student, KiberonStudentReg
from .services import form_data_processing, get_response_for_create_group, \
    get_response_for_create_student, get_response_for_remove_group, \
    get_response_for_remove_student, get_response_for_remove_kiberon_reg, get_days_of_week, get_groups_by_day_of_week


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
        days_of_week = get_days_of_week(tutor=self.request.user)
        context['groups_by_days'] = []
        for day_of_week in days_of_week:
            groups_for_day_of_week = get_groups_by_day_of_week(day_of_week=day_of_week, tutor=self.request.user)
            context['groups_by_days'].append(groups_for_day_of_week)

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
    login_url = reverse_lazy('authapp:login')
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
        context['update_students_forms'] = tuple(UpdateStudentForm(instance=student) for student in context['students'])
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


class UpdateStudentView(UpdateView, LoginRequiredMixin):
    """Обновление студента"""
    login_url = reverse_lazy('authapp:login')
    model = Student
    form_class = UpdateStudentForm
    require_http_methods = ['POST']


class RemoveStudent(DeleteView, LoginRequiredMixin):
    """Прдеставление для удаления студента"""
    login_url = reverse_lazy('authapp:login')

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
        result = form_data_processing(data=form.cleaned_data, tutor=request.user)
        for success_message in result['success']:
            messages.success(request, success_message)
        for error_message in result['error']:
            messages.error(request, error_message)
    else:
        messages.error(request, 'Необходимо выделить хотя бы одного ученика')
    return HttpResponseRedirect(reverse_lazy('mainapp:student-list',
                                             kwargs={'group_id': group_id}))


class KiberonLogList(ListView, LoginRequiredMixin):
    """ Журнал печатей """
    template_name = 'mainapp/kiberon_reg/list.html'
    model = KiberonStudentReg
    paginate_by = 30
    context_object_name = 'kiberon_regs'

    def get_queryset(self):
        return KiberonStudentReg.objects.filter(tutor=self.request.user).select_related('student', 'kiberon')


def search_reg(request):
    """ фильтрация печатей """
    result = KiberonStudentReg.objects.filter(student__name__icontains=request.GET.get('name'))[:50]
    return JsonResponse({'markup': render_to_string('mainapp/includes/kiberon_regs.html', {'kiberon_regs': result})})


class KiberonRegDelete(DeleteView, LoginRequiredMixin):
    """ удаление записи о киберонах из журнала """
    require_http_methods = ['post']

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_remove_kiberon_reg(reg_id=body.get('reg_id'))
