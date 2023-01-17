from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, \
    PasswordChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from mainapp.models import Group, Student


class LoginForm(AuthenticationForm):
    """Форма входа на сайт"""
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label="E-mail")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class TutorPasswordChangeForm(PasswordChangeForm):
    pass


class TutorPasswordResetForm(PasswordResetForm):
    pass


class StudentLoginForm(forms.Form):
    '''
    Форма авторизации ученика
    '''
    group_key = forms.CharField(
        label=_('Код группы'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_("Код ученика"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    
    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            group = Group.objects.get(slug=cleaned_data.get('group_key'))
        except Group.DoesNotExist:
            raise ValidationError(_('Такой группы не существует'))
        try:
            student = Student.objects.get(
                code=cleaned_data.get('password')
            )
        except Student.DoesNotExist:
            raise ValidationError(_('Такого ученика не существует'))
        if student.group.slug != group.slug:
            raise ValidationError(_('Вы не состоите в этой группе'))
        return cleaned_data

