from authapp.models import Tutor

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Group, Student, KiberonStudentReg, Kiberon


def get_response_for_remove_group(group_id: str, password: str,
                                  username: str) -> JsonResponse:
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


def get_response_for_create_group(time: str, location: str,
                                  day_of_week: str, user: Tutor) -> \
        JsonResponse:
    """Получаем ответ для запроса создания группы"""
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
                         day_of_week=day_of_week, tutor=user)
    return JsonResponse({'success': True,
                         'redirect': reverse_lazy('mainapp:groups')})


def get_response_for_create_student(name: str, kiberon_amount: int,
                                    info: str, group_id: int) -> JsonResponse:
    """Получаем ответ при отправке формы добавления студента"""
    Student.objects.create(name=name, kiberon_amount=kiberon_amount,
                           info=info, group_id=group_id)
    redirect = reverse_lazy('mainapp:group-detail', kwargs={'pk': group_id})
    return JsonResponse({'success': True, 'redirect': redirect})


def get_response_for_remove_student(student_id: str, password: str,
                                    username: str) -> JsonResponse:
    """Получаем ответ для запроса удаления студента"""
    student = get_object_or_404(Student, pk=student_id)
    if student is not None:
        if student.is_deleted:
            return JsonResponse({'success': False,
                                 'message': 'Студент уже удален'})
        user = authenticate(username=username, password=password)
        if user is not None:
            student.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False,
                             'message': 'Неверный пароль'})
    return JsonResponse({'success': False,
                         'message': 'Изменилось id '
                                    'студента или где-то'
                                    ' в другом месте его удалили, '
                                    'обнови странццу'})


def form_data_processing(data: dict, tutor: Tutor) -> None:
    """Обработка массового обновления учеников"""
    students = Student.objects.filter(pk__in=data.get('student_ids')
                                      .split(','))
    kiberon = Kiberon.objects.get(achievement=data.get('action'))
    for student in students:
        KiberonStudentReg.objects.create(student=student, kiberon=kiberon,
                                         tutor=tutor)
