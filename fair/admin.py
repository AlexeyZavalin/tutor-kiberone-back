from django.contrib import admin
from fair.models import FairRegistration, Souvenir


@admin.register(Souvenir)
class SouvenirAdmin(admin.ModelAdmin):
    """ Админка сувенира """
    list_display = ['name', 'is_deleted']


@admin.register(FairRegistration)
class FairRegistration(admin.ModelAdmin):
    """ Админка записи о ярмарке """
    date_hierarchy = 'date'
    list_filter = ['student__group__tutor', 'student__group', 'date']
    search_fields = ['student__name', 'name']
