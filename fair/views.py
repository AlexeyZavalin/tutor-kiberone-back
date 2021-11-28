from django.shortcuts import render

from django.views.generic.list import ListView

from fair.models import Souvenir


class SouvenirsListView(ListView):
    """ Список сувениров """
    model = Souvenir
    context_object_name = 'souvenirs'
    template_name = 'fair/souvenir/list.html'
    queryset = Souvenir.objects.filter(is_deleted=False)
