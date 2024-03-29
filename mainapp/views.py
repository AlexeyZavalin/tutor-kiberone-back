import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import BulkStudentActionsForm, CreateStudentForm, \
    RemoveGroupForm, RemoveStudentForm, UpdateStudentForm, \
    CreateUpdateGroupForm, CustomKiberonAddForm, \
    FilterStudentsForm, CustomKiberonRemoveForm
from .mixins import StudentRequiredMixin
from .models import Group, Student, KiberonStudentReg, SiteConfiguration
from .services import form_data_processing, get_response_for_create_group, \
    get_response_for_create_student, get_response_for_remove_group, \
    get_response_for_remove_student, get_response_for_remove_kiberon_reg, \
    get_days_of_week, get_groups_by_day_of_week, \
    get_response_for_custom_adding_kiberons, \
    get_response_for_custom_remove_kiberons


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

    def get_queryset(self):
        return Group.active.filter(tutor=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        days_of_week = get_days_of_week(tutor=self.request.user)
        context['groups_by_days'] = []
        for day_of_week in days_of_week:
            groups_for_day_of_week = get_groups_by_day_of_week(
                day_of_week=day_of_week, tutor=self.request.user)
            context['groups_by_days'].append(groups_for_day_of_week)
        context['update_group_forms'] = tuple(
            CreateUpdateGroupForm(instance=group) for group in
            context['groups'])
        context['remove_form'] = RemoveGroupForm()
        context['create_group_form'] = CreateUpdateGroupForm()
        return context


class RemoveGroup(LoginRequiredMixin, DeleteView):
    """Прдеставление для удаления группы"""

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_remove_group(group_id=body.get('group_id'),
                                             password=body.get('password'),
                                             username=request.user.email)


class CreateGroupView(LoginRequiredMixin, CreateView):
    """Представление для создания группы"""
    login_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_create_group(location=body.get('location'),
                                             time=body.get('time'),
                                             day_of_week=body.get(
                                                 'day_of_week'),
                                             user=request.user)


class UpdateGroupView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    """Обновление группы"""
    login_url = reverse_lazy('authapp:login')
    model = Group
    form_class = CreateUpdateGroupForm
    success_url = reverse_lazy('mainapp:groups')
    url = reverse_lazy('mainapp:groups')

    def form_invalid(self, form):
        messages.error(self.request, 'Такая группа уже есть')
        return HttpResponseRedirect(reverse_lazy('mainapp:groups'))

    def form_valid(self, form):
        messages.success(self.request, 'Группа обновлена')
        return super().form_valid(form)


class StudentListView(LoginRequiredMixin, ListView):
    """Список студентов группы"""
    login_url = reverse_lazy('authapp:login')
    model = Student
    template_name = 'mainapp/student/list.html'
    student_list_template = 'mainapp/includes/student_list.html'
    context_object_name = 'students'

    def filter(self, queryset):
        if self.request.GET.get('visited_today'):
            visited_today = self.request.GET.get('visited_today')
            if visited_today == '1':
                self.request.session['visited_today'] = True
                queryset = queryset.filter(visited_date=date.today())
            elif visited_today == '0':
                if 'visited_today' in self.request.session:
                    del self.request.session['visited_today']
        if self.request.session.get('visited_today'):
            queryset = queryset.filter(visited_date=date.today())
        return queryset

    def get(self, request, *args, **kwargs):
        # TODO: снизу код отвратительный нужно будет его править в любом случае
        config = SiteConfiguration.get_solo()
        if request.GET.get('sort_by'):
            sort_order = request.GET.get('sort_order')
            sort_by = request.GET.get('sort_by')
            if sort_order == 'DESC':
                sort_by = f'-{sort_by}'
            queryset = Student.active.filter(group_id=self.kwargs.get(
                'group_id')).order_by(sort_by)
            queryset = self.filter(queryset)
            context = {
                'students': queryset,
                'request': request,
                'fair_is_active': config.fair_is_active
            }
            template = render_to_string(
                self.student_list_template, context
            )
            return JsonResponse({'markup': template})
        if request.GET.get('visited_today'):
            queryset = Student.active.filter(group_id=self.kwargs.get(
                'group_id')).order_by('kiberon_amount')
            queryset = self.filter(queryset)
            context = {
                'students': queryset,
                'request': request,
                'fair_is_active': config.fair_is_active
            }
            template = render_to_string(
                self.student_list_template, context
            )
            return JsonResponse({'markup': template})
        result = super(StudentListView, self).get(request, *args, **kwargs)
        return result

    def get_queryset(self):
        queryset = Student.active.filter(group_id=self.kwargs.get(
            'group_id')).order_by('-kiberon_amount')
        queryset = self.filter(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(pk=self.kwargs.get('group_id'))
        context['create_student_form'] = CreateStudentForm()
        context['remove_student_form'] = RemoveStudentForm()
        context['update_students_forms'] = tuple(
            UpdateStudentForm(instance=student, auto_id=False)
            for student in context['students']
        )
        context['bulk_action_form'] = BulkStudentActionsForm()
        initial_filters = {'visited_today': '0'}
        if 'visited_today' in self.request.session and \
                self.request.session.get('visited_today'):
            initial_filters['visited_today'] = '1'
        context['custom_kiberon_form'] = CustomKiberonAddForm(prefix='add')
        context['custom_kiberon_remove_form'] = CustomKiberonRemoveForm(
            prefix='remove',
        )
        context['filter_students_form'] = FilterStudentsForm(
            initial=initial_filters)
        return context


class CreateStudentView(LoginRequiredMixin, CreateView):
    """Представление для добавления студента в группу"""

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_create_student(name=body.get('name'),
                                               kiberon_amount=body.get(
                                                   'kiberon_amount', 0),
                                               info=body.get('info'),
                                               group_id=kwargs.get('group_id'))


class UpdateStudentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Обновление студента"""
    login_url = reverse_lazy('authapp:login')
    model = Student
    form_class = UpdateStudentForm
    require_http_methods = ['POST']

    def get_success_message(self, cleaned_data):
        return f'Ученик {self.get_object().name} успешно обновлен'


class CreateCustomKiberonRegView(LoginRequiredMixin, CreateView):
    """Создаем запись в журнале с кастомным количеством киберонов"""
    form_class = CustomKiberonAddForm

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        kiberon_amount = body.get('kiberon_amount')
        student_id = int(body.get('student_id'))
        achievement = body.get('achievement')
        response = get_response_for_custom_adding_kiberons(
            kiberon_amount=kiberon_amount,
            student_id=student_id,
            achievement=achievement,
            group_id=kwargs.get('group_id'),
            tutor=self.request.user
        )
        if response.status_code == 200:
            student = Student.objects.get(pk=int(body.get('student_id')))
            message = f'{student.name} - {kiberon_amount}к - достижение ' \
                      f'"{achievement}"'
            messages.success(self.request, message)
        return response


class RemoveCustomKiberonRegView(LoginRequiredMixin, View):
    """Представление для удаления киберонов"""

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_custom_remove_kiberons(
            kiberon_amount=body.get('kiberon_amount'),
            student_id=int(body.get(
                'student_id')),
            group_id=kwargs.get('group_id'))


class RemoveStudentView(LoginRequiredMixin, DeleteView):
    """Прдеставление для удаления студента"""
    login_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_remove_student(
            student_id=body.get('student_id'),
            password=body.get('password'),
            username=request.user.email
        )


@require_http_methods(['POST'])
def bulk_update_students(request, group_id):
    """Представление для массовой обработки студентов"""
    form = BulkStudentActionsForm(request.POST)
    if form.is_valid():
        result = form_data_processing(data=form.cleaned_data,
                                      tutor=request.user)
        for success_message in result['success']:
            messages.success(request, success_message)
        for error_message in result['error']:
            messages.error(request, error_message)
    else:
        messages.error(request, 'Необходимо выделить хотя бы одного ученика')
    return HttpResponseRedirect(reverse_lazy('mainapp:student-list',
                                             kwargs={'group_id': group_id}))


class KiberonLogList(LoginRequiredMixin, ListView):
    """ Журнал печатей """
    template_name = 'mainapp/kiberon_reg/list.html'
    model = KiberonStudentReg
    paginate_by = 30
    context_object_name = 'kiberon_regs'

    def get_queryset(self):
        return KiberonStudentReg.objects.filter(
            tutor=self.request.user).select_related('student', 'kiberon')


def search_reg(request):
    """ фильтрация печатей """
    result = KiberonStudentReg.objects.filter(
        student__name__icontains=request.GET.get('name'), tutor=request.user)[
             :50]
    return JsonResponse({'markup': render_to_string(
        'mainapp/includes/kiberon_regs.html', {'kiberon_regs': result})})


class KiberonRegDelete(LoginRequiredMixin, DeleteView):
    """ удаление записи о киберонах из журнала """
    require_http_methods = ['post']

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        return get_response_for_remove_kiberon_reg(reg_id=body.get('reg_id'))


class StudentPersonalArea(StudentRequiredMixin, DetailView):
    '''
    личная страница ученика
    '''

    login_url = reverse_lazy('authapp:login_student')
    template_name = 'mainapp/student/detail.html'
    context_object_name = 'student'

    def dispatch(self, request, *args, **kwargs):
        if not request.student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.student

    def get_context_data(self, **kwargs):
        data = super(StudentPersonalArea, self).get_context_data(**kwargs)
        data['last_achievements'] = KiberonStudentReg.objects.filter(
            student=data.get('object'))[:5]
        return data


class StudentGroup(StudentRequiredMixin, ListView):
    '''
   страница группы ученика
   '''
    login_url = reverse_lazy('authapp:login_student')
    model = Student
    template_name = 'mainapp/group/detail.html'
    student_list_template = 'mainapp/includes/student_list.html'
    context_object_name = 'students'

    def dispatch(self, request, *args, **kwargs):
        if not request.student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Student.active.filter(group=self.request.student.group) \
            .order_by('-kiberon_amount')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.request.student.group
        context['student'] = self.request.student
        return context
