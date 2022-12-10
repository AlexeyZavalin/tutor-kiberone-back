import json

from django.http import JsonResponse
from django.core import serializers

from django.views import View

from fair.models import Souvenir, FairRegistration
from fair.services import get_response_for_create_fair
from mainapp.models import Student


def souvenirs_list(request):
    """
        список киберприятностей
    """
    objects = Souvenir.objects.filter(is_deleted=False, amount__gt=0)
    if 'id' in request.GET:
        student = Student.objects.get(id=request.GET['id'])
        objects = objects.filter(
            price__lte=student.kiberon_amount,
        )

    return JsonResponse(serializers.serialize('json', objects), safe=False)


class FairRegistrationCreateView(View):
    """
    Представление для создания записи о проведенной ярмарке для ученика
    """
    model = FairRegistration

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        items = body['items']
        student_id = body['studentId']
        balance = body['balance']
        total = body['cart']['total']
        return get_response_for_create_fair(student_id=student_id,
                                            items=items, balance=balance,
                                            total=total)
