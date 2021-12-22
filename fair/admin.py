from django.contrib import admin
from django.db.models import Sum

from fair.models import FairRegistration, FairRegistrationSouvenir, Souvenir


class SouvenirInline(admin.StackedInline):
    model = FairRegistrationSouvenir
    readonly_fields = ['price']
    exclude = ['souvenir']
    extra = 0
    can_delete = False
    verbose_name = 'Сувенир'
    verbose_name_plural = 'Сувениры'


@admin.register(Souvenir)
class SouvenirAdmin(admin.ModelAdmin):
    """ Админка сувенира """
    list_display = ['name', 'price', 'amount', 'is_deleted']
    extra = 0


@admin.register(FairRegistration)
class FairRegistration(admin.ModelAdmin):
    """ Админка записи о ярмарке """
    date_hierarchy = 'date'
    list_filter = ['student__group__tutor', 'student__group', 'date']
    search_fields = ['student__name']
    list_display = ['student', 'date']
    readonly_fields = ['student', 'date', 'total']
    inlines = [SouvenirInline]

    def total(self, object):
        """ получаем сумму в киберонах """
        return object.souvenirs.all().aggregate(Sum('price')).get('price__sum')

    total.short_description = 'Всего потрачено'
