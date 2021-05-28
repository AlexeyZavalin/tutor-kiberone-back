from django.contrib import admin

from mainapp.models import Group, Student, Kiberon, KiberonStudentReg, Tutor


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'time', 'location', 'tutor']
    list_filter = ['tutor', 'day_of_week']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['group']


@admin.register(Kiberon)
class KiberonAdmin(admin.ModelAdmin):
    list_display = ['achievement']


@admin.register(KiberonStudentReg)
class KiberonStudentRegAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email']
