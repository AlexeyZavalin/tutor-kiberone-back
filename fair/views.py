import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from django.template.loader import render_to_string
from django.views import View

from fair.models import Souvenir, FairRegistration
from fair.services import get_response_for_create_fair
from mainapp.models import Student


@login_required
def souvenirs_list(request):
    """
        список киберприятностей
    """
    qs = Souvenir.objects.filter(is_deleted=False, amount__gt=0)
    if 'id' in request.GET:
        try:
            student = Student.objects.get(id=request.GET['id'])
            qs = qs.filter(price__lte=student.kiberon_amount)
        except ObjectDoesNotExist:
            # ученик не найден
            pass
    template = render_to_string(
        'fair/souvenir/list.html', {'souvenirs': qs}
    )
    return JsonResponse({'markup': template})


class FairRegistrationCreateView(View, LoginRequiredMixin):
    """
    Представление для создания записи о проведенной ярмарке для ученика
    """
    model = FairRegistration

    def post(self, *args, **kwargs):
        body = json.loads(self.request.body)
        items = body['items']
        student_id = body['studentId']
        balance = body['balance']
        total = body['cart']['total']
        return get_response_for_create_fair(student_id=student_id,
                                            items=items, balance=balance,
                                            total=total)
