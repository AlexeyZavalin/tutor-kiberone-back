from django.contrib import admin

from fair.models import FairRegistration, FairRegistrationSouvenir, Souvenir, \
    Refund


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
class FairRegistrationAdmin(admin.ModelAdmin):
    """ Админка записи о ярмарке """
    date_hierarchy = 'date'
    list_filter = ['student__group__tutor', 'student__group', 'date']
    search_fields = ['student__name']
    list_display = ['student', 'date']
    readonly_fields = ['student', 'date', 'total']
    inlines = [SouvenirInline]

    def total(self, object):
        """ получаем сумму в киберонах """
        return object.total

    total.short_description = 'Всего потрачено'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    '''
    Админка возвратов
    '''
    raw_id_fields = ['fair_registration']
    list_display = ['__str__', 'complete']
