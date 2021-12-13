from django.contrib import admin
from solo.admin import SingletonModelAdmin

from mainapp.models import Group, Student, Kiberon, KiberonStudentReg,\
    SiteConfiguration


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'time', 'location', 'tutor']
    list_filter = ['tutor', 'day_of_week']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'kiberon_amount']
    ordering = ['kiberon_amount']
    search_fields = ['name']
    list_filter = ['group', 'group__tutor']


@admin.register(Kiberon)
class KiberonAdmin(admin.ModelAdmin):
    list_display = ['achievement']


@admin.register(KiberonStudentReg)
class KiberonStudentRegAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    date_hierarchy = 'date'
    search_fields = ['student__name']
    list_filter = ['tutor', 'kiberon']


admin.site.register(SiteConfiguration, SingletonModelAdmin)
