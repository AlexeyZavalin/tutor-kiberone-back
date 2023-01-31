from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from authapp.models import Tutor

from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Group, Student, KiberonStudentReg, Kiberon


def get_response_for_remove_group(
    group_id: str,
    password: str,
    username: str
) -> JsonResponse:
    """Получаем ответ для запроса удаления группы"""
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


def get_response_for_create_group(
    time: str,
    location: str,
    day_of_week: str,
    user: Tutor
) -> JsonResponse:
    """Получаем ответ для запроса создания группы"""
    group = Group.objects.filter(
        available_time_id=time,
        available_location_id=location,
        day_of_week=day_of_week
    )
    if group.exists():
        if group.first().is_deleted:
            group.update(is_deleted=False)
            return JsonResponse({'success': True,
                                 'redirect':
                                     reverse_lazy('mainapp:groups')})
        return JsonResponse({'success': False,
                             'message': 'Такая группа уже есть, '
                                        'измените параметры'})
    Group.objects.create(
        available_location_id=location,
        available_time_id=time,
        day_of_week=day_of_week,
        tutor=user
    )
    return JsonResponse({'success': True,
                         'redirect': reverse_lazy('mainapp:groups')})


def get_response_for_create_student(
    name: str,
    info: str,
    group_id: int,
    kiberon_amount: int = 0
) -> JsonResponse:
    """Получаем ответ при отправке формы добавления студента"""
    Student.objects.create(name=name, kiberon_amount=kiberon_amount,
                           info=info, group_id=group_id)
    redirect = reverse_lazy('mainapp:student-list',
                            kwargs={'group_id': group_id})
    return JsonResponse({'success': True, 'redirect': redirect})


def get_response_for_remove_student(
    student_id: int,
    password: str,
    username: str
) -> JsonResponse:
    """Получаем ответ для запроса удаления студента"""
    student = get_object_or_404(Student, pk=student_id)
    if student is not None:
        if student.is_deleted:
            return JsonResponse({'success': False,
                                 'message': 'Студент уже удален'})
        user = authenticate(username=username, password=password)
        if user is not None:
            student.delete()
            return JsonResponse(
                {'success': True, 'message': 'Студент успешно удален'})
        return JsonResponse({'success': False,
                             'message': 'Неверный пароль'})
    return JsonResponse({'success': False,
                         'message': 'Изменилось id '
                                    'студента или где-то'
                                    ' в другом месте его удалили, '
                                    'обнови странццу'})


def form_data_processing(data: dict, tutor: Tutor) -> dict:
    """Обработка массового обновления учеников
    Получаем словарь с информацией о добавлении записей"""
    students = Student.objects.filter(pk__in=data.get('student_ids')
                                      .split(','))
    messages = {
        'success': [],
        'error': []
    }
    try:
        kiberon = Kiberon.objects.get(achievement=data.get('action'))
        for student in students:
            try:
                KiberonStudentReg.objects.create(student=student,
                                                 kiberon=kiberon, tutor=tutor)
                messages['success'].append(
                    f'{student.name} - {kiberon.value}к - '
                    f'достижение "{kiberon.get_achievement_display()}"')
            except IntegrityError:
                # запись уже есть
                messages['error'].append(
                    f'для {student.name} запись с достижением на текущую дату '
                    f'"{kiberon.get_achievement_display()}" уже есть')
    except ObjectDoesNotExist:
        # такого не должно случиться, но на всякий случай, вдруг как-то исчезнет киберон
        messages['error'].append('Такого достижения нет')
    return messages


def get_response_for_remove_kiberon_reg(reg_id: int) -> JsonResponse:
    """Получаем ответ для удаления записи из журнала киберонов"""
    try:
        KiberonStudentReg.objects.get(pk=reg_id).delete()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False})


def get_days_of_week(tutor: Tutor) -> tuple:
    """Получаем доступные дни недели"""
    days_of_week = Group.active.filter(
        Q(tutor=tutor) | Q(temporary_tutor=tutor)).distinct() \
        .values_list('day_of_week', flat=True)
    return tuple(
        day_of_week[0] for day_of_week in Group.DAYS_OF_WEEK_CHOICES if
        day_of_week[0] in days_of_week)


def get_groups_by_day_of_week(day_of_week: str, tutor: Tutor) -> dict:
    """получем словарь ловарь с днем недели и группами для этого дня"""

    groups = Group.active.filter(Q(tutor=tutor) | Q(temporary_tutor=tutor),
                                 day_of_week=day_of_week)\
        .order_by('available_time')
    _, day_of_week_display = [day for day in Group.DAYS_OF_WEEK_CHOICES
                              if day[0] == day_of_week][0]
    return {
        'day_of_week': day_of_week_display,
        'groups': groups
    }


def get_response_for_custom_adding_kiberons(
    kiberon_amount: int,
    student_id: int,
    group_id: int,
    achievement: str,
    tutor: Tutor
) -> JsonResponse:
    """Получаем ответ для кастомного добавления киберонов"""
    try:
        student = Student.objects.get(pk=student_id)
        redirect = reverse_lazy('mainapp:student-list',
                                kwargs={'group_id': group_id})
        kiberon = Kiberon.objects.get(achievement=Kiberon.CUSTOM)
        KiberonStudentReg.objects.create(
            student=student,
            kiberon=kiberon,
            custom_kiberons=kiberon_amount,
            custom_achievement=achievement,
            tutor=tutor
        )
        return JsonResponse(
            {
                'success': True,
                'redirect': redirect,
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'Такого ученика нет'
            },
            status=500
        )
    except IntegrityError:
        return JsonResponse(
            {
                'success': False,
                'message': 'Что-то пошло не так'
            },
            status=500
        )


def get_response_for_custom_remove_kiberons(
    kiberon_amount: int,
    student_id: int,
    group_id: int
) -> JsonResponse:
    """Получаем ответ для удаления киберонов"""
    try:
        student = Student.objects.get(pk=student_id)
        redirect = reverse_lazy('mainapp:student-list',
                                kwargs={'group_id': group_id})
        student.delete_kiberons(kiberon_amount)
        return JsonResponse({'success': True, 'redirect': redirect})
    except ObjectDoesNotExist:
        return JsonResponse(
            {'success': False, 'message': 'Такого ученика нет'})
    except IntegrityError:
        return JsonResponse(
            {'success': False, 'message': 'Что-то пошло не так'})
