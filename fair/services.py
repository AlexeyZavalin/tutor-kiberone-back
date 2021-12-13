from decimal import Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy

from fair.models import Souvenir, FairRegistration, FairRegistrationSouvenir
from mainapp.models import Student


def get_response_for_create_fair(student_id: int, items: list, balance: int,
                                 total: int) -> JsonResponse:
    """
    student_id: id ученика
    items: список id сувениров
    balance: остаток киберонов у ученика
    total: сумма киберонов по сувенирам
    """
    try:
        student = Student.objects.get(pk=student_id)
        souvenirs = Souvenir.objects.filter(pk__in=items)
        assert Decimal(total) == souvenirs.aggregate(Sum('price')).get(
            'price__sum')
        order = FairRegistration.objects.create(student=student)
        student.delete_kiberons(total)
        # создаем
        for souvenir in souvenirs:
            FairRegistrationSouvenir.objects.create(souvenir=souvenir,
                                                    price=souvenir.price,
                                                    fair_registration=order)
        redirect = reverse_lazy('mainapp:student-list',
                                kwargs={'group_id': student.group.pk})
        return JsonResponse({'success': True, 'redirect': redirect})
    except Student.DoesNotExist:
        return JsonResponse(
            {'success': False, 'message': 'Такого ученика нет'})
    except AssertionError:
        return JsonResponse(
            {'success': False, 'message': 'Ошибка в балансе'})
