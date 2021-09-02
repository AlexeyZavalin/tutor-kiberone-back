from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Group, Student, Kiberon


class RemoveGroupForm(forms.Form):
    """Форма для удаления группы"""
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    group_id = forms.CharField(widget=forms.HiddenInput)


class CreateGroupForm(forms.ModelForm):
    """Форма для создания группы"""

    class Meta:
        model = Group
        fields = ['time', 'location', 'day_of_week']


class CreateStudentForm(forms.ModelForm):
    """Форма добавления студента в группу"""

    class Meta:
        model = Student
        fields = ['name', 'kiberon_amount', 'info']


class UpdateStudentForm(CreateStudentForm):
    """Форма добавления студента в группу"""

    class Meta:
        model = Student
        fields = ['name', 'info']


class RemoveStudentForm(forms.Form):
    """Форма для удаления студента"""
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    student_id = forms.CharField(widget=forms.HiddenInput)


class BulkStudentActionsForm(forms.Form):
    """Форма массовых действий с ученикми"""
    ACTION_CHOICES = (
        (Kiberon.VISIT, 'Поставить кибероны за посещение'),
        (Kiberon.EYES, 'Поставить кибероны за разминку для глаз'),
    )
    action = forms.ChoiceField(label='Действия', required=True,
                               choices=ACTION_CHOICES)
    student_ids = forms.CharField(widget=forms.HiddenInput)
