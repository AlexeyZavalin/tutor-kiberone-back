from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Group, Student, Kiberon, SiteConfiguration


class RemoveGroupForm(forms.Form):
    """Форма для удаления группы"""
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    group_id = forms.CharField(widget=forms.HiddenInput)


class CreateUpdateGroupForm(forms.ModelForm):
    """Форма для создания группы"""

    class Meta:
        model = Group
        fields = ['available_time', 'available_location', 'day_of_week',
                  'temporary_tutor']


class CreateStudentForm(forms.ModelForm):
    """Форма добавления студента в группу"""

    class Meta:
        model = Student
        fields = ['name', 'info']


class UpdateStudentForm(CreateStudentForm):
    """Форма добавления студента в группу"""

    class Meta:
        model = Student
        fields = ['name', 'info', 'gmail_name']


class RemoveStudentForm(forms.Form):
    """Форма для удаления студента"""
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    remove_student_id = forms.CharField(widget=forms.HiddenInput)


class BulkStudentActionsForm(forms.Form):
    """Форма массовых действий с ученикми"""
    ACTION_CHOICES = [choice for choice in Kiberon.ACHIEVEMENT_CHOICES
                      if choice[0] != Kiberon.CUSTOM]
    action = forms.ChoiceField(
        label='Действия',
        required=True,
        choices=ACTION_CHOICES
    )
    student_ids = forms.CharField(widget=forms.HiddenInput)


class CustomKiberonAddForm(forms.Form):
    """Форма для добавления костомного количества киберонов"""
    achievement = forms.CharField(
        max_length=100,
        label='Достижение',
        required=True
    )
    kiberons_amount = forms.IntegerField()
    student_id = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kiberons_amount'] = forms.IntegerField(
            max_value=SiteConfiguration.get_solo().max_custom_kiberons,
            min_value=1,
            label='Количество киберонов',
            initial=5
        )


class CustomKiberonRemoveForm(forms.Form):
    """Форма для удалени киберонов"""
    kiberons_amount = forms.IntegerField()
    student_id = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kiberons_amount'] = forms.IntegerField(
            max_value=SiteConfiguration.get_solo().max_custom_kiberons,
            label='Количество киберонов',
            min_value=5,
            initial=5
        )


class FilterStudentsForm(forms.Form):
    """Форма для фильтрации студентов"""
    VISITED = 1
    ALL = 0
    CHOICES = (
        (VISITED, 'Посетили сегодня'),
        (ALL, 'Все')
    )
    visited_today = forms.ChoiceField(
        label='Присутствуют сегодня',
        required=False,
        choices=CHOICES
    )
